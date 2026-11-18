import asyncio
import math
import time

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import (
    is_learned, get_user, get_current_task,
    set_current_task, clear_current_task, increment_stats,
)
from utils import (
    generate_task, check_answer, correct_answer,
    LEVELS, get_next_level,
)
from keyboards import tasks_keyboard
from handlers.cabinet import build_cabinet_text

router = Router()

_active_timers: dict[int, asyncio.Task] = {}


def _cancel_timer(telegram_id: int):
    task = _active_timers.pop(telegram_id, None)
    if task and not task.done():
        task.cancel()


async def _timer_worker(bot, telegram_id: int, number: int, deadline: float):
    try:
        delay = deadline - time.time()
        if delay > 0:
            await asyncio.sleep(delay)

        current = await get_current_task(telegram_id)
        if not current or current['number'] != number:
            return

        await increment_stats(telegram_id, False)
        await clear_current_task(telegram_id)

        correct = math.sqrt(number)
        try:
            await bot.send_message(
                telegram_id,
                f"⏱ <b>Время вышло!</b>\n"
                f"Правильный ответ: √{number} ≈ {correct:.4f}",
                reply_markup=tasks_keyboard(),
                parse_mode="HTML",
            )
        except Exception:
            pass
    except asyncio.CancelledError:
        pass
    finally:
        _active_timers.pop(telegram_id, None)


async def _issue_task(telegram_id: int, bot) -> str:
    user = await get_user(telegram_id)
    total_done = user['correct_answers'] + user['incorrect_answers']
    correct = user['correct_answers']
    level = get_next_level(total_done, correct)
    task = generate_task(level)

    time_limit = LEVELS[level]['time_limit']
    deadline = time.time() + time_limit
    await set_current_task(telegram_id, task['number'], task['precision'], deadline)

    _cancel_timer(telegram_id)
    _active_timers[telegram_id] = asyncio.create_task(
        _timer_worker(bot, telegram_id, task['number'], deadline)
    )

    return (
        f"📝 <b>Задача #{total_done + 1}</b>\n"
        f"Уровень: {LEVELS[level]['name']}\n"
        f"⏱ Время: <b>{time_limit} сек</b>\n\n"
        f"Найди <b>√{task['number']}</b> с точностью до <b>{task['precision']}</b>\n\n"
        f"Введи ответ числом:"
    )


def _build_stats_text(user) -> str:
    total_done = user['correct_answers'] + user['incorrect_answers']
    return (
        f"📊 <b>Твоя статистика</b>\n\n"
        f"💼 Всего задач: <b>{total_done}</b>\n"
        f"✅ Правильных: <b>{user['correct_answers']}</b>\n"
        f"❌ Неправильных: <b>{user['incorrect_answers']}</b>\n\n"
        f"Выбери действие:"
    )


@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    if not await is_learned(message.from_user.id):
        await message.answer("⚠️ Сначала пройди обучение! Введи /learn")
        return

    current = await get_current_task(message.from_user.id)
    if current and current['deadline'] and time.time() >= current['deadline']:
        _cancel_timer(message.from_user.id)
        await increment_stats(message.from_user.id, False)
        await clear_current_task(message.from_user.id)
        current = None

    user = await get_user(message.from_user.id)
    text = _build_stats_text(user)

    if current:
        remaining = int(current['deadline'] - time.time()) if current['deadline'] else 0
        text += (
            f"\n\n⏱ У тебя есть активная задача:\n"
            f"√{current['number']} (осталось <b>{remaining} сек</b>)"
        )

    await message.answer(text, reply_markup=tasks_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "get_task")
async def get_task(callback: CallbackQuery):
    if not await is_learned(callback.from_user.id):
        await callback.answer("Сначала пройди /learn", show_alert=True)
        return

    current = await get_current_task(callback.from_user.id)
    if current:
        if current['deadline'] and time.time() < current['deadline']:
            remaining = int(current['deadline'] - time.time())
            await callback.message.answer(
                f"У тебя уже есть активная задача:\n"
                f"<b>√{current['number']}</b> с точностью до <b>{current['precision']}</b>\n"
                f"⏱ Осталось: <b>{remaining} сек</b>",
                parse_mode="HTML",
            )
            await callback.answer()
            return
        _cancel_timer(callback.from_user.id)
        await increment_stats(callback.from_user.id, False)
        await clear_current_task(callback.from_user.id)

    text = await _issue_task(callback.from_user.id, callback.bot)
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "to_cabinet")
async def to_cabinet(callback: CallbackQuery):
    text = await build_cabinet_text(callback.from_user.id)
    if text is None:
        await callback.message.answer("Сначала нажми /start")
    else:
        await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


@router.message(F.text & ~F.text.startswith("/"))
async def handle_answer(message: Message):
    task = await get_current_task(message.from_user.id)
    if not task:
        await message.answer("Сначала введи /tasks и нажми «Получить задачу».")
        return

    if task['deadline'] and time.time() > task['deadline']:
        _cancel_timer(message.from_user.id)
        await increment_stats(message.from_user.id, False)
        await clear_current_task(message.from_user.id)
        correct = correct_answer(task)
        await message.answer(
            f"⏱ <b>Время вышло!</b> Правильный ответ: "
            f"√{task['number']} ≈ {correct:.4f}",
            reply_markup=tasks_keyboard(),
            parse_mode="HTML",
        )
        return

    try:
        user_answer = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer("Это не число. Введи ответ числом, например: 7.07")
        return

    _cancel_timer(message.from_user.id)
    is_correct = check_answer(user_answer, task)
    await increment_stats(message.from_user.id, is_correct)
    await clear_current_task(message.from_user.id)

    correct = correct_answer(task)
    if is_correct:
        result = f"✅ <b>Верно!</b> √{task['number']} ≈ {correct:.4f}"
    else:
        result = f"❌ <b>Неверно.</b> Правильный ответ: √{task['number']} ≈ {correct:.4f}"

    await message.answer(result, reply_markup=tasks_keyboard(), parse_mode="HTML")