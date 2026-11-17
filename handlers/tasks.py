# handlers/tasks.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import is_learned, get_user, get_current_task, crear_current_task, increment_stats, set_current_task
from utils import generate_task, check_answer, correct_answer, LEVELS, get_callibration_level

router = Router()


async def _issue_task(telegram_id: int) -> str:
    user = await get_user(telegram_id)
    total_done = user['correct_answers'] + user['incorrecct_answers']
    level = get_callibration_level(total_done)
    task = generate_task(level)
    await set_current_task(telegram_id, task['number'], task['precision'])

    return (
        f"📝 <b>Задача #{total_done + 1}</b>\n"
        f"Уровень: {LEVELS[level]['name']}\n\n"
        f"Найди <b>√{task['number']}</b> с точностью до <b>{task['precision']}</b>\n\n"
        f"Введи ответ числом:"
    )


@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    if not await is_learned(message.from_user.id):
        await message.answer(
            "⚠️ Сначала пройди обучение!\n"
            "Для этого используй /learn"
        )
        return
    await message.answer("В разработке")