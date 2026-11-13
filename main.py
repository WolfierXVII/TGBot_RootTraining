import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import src_private
from database import init_db, add_user, get_user, get_total_users, get_user_rank

logging.basicConfig(level=logging.INFO)

bot = Bot(token=src_private.bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await add_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name
    )
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")]],resize_keyboard=True)
    await message.answer(f"Приветствую тебя,{message.from_user.full_name}!\n"
                         f"При помощи данного бота ты сможешь обучиться считать приближённые корни чисел!\n"
                         f"Готов начать?",
                         reply_markup=kb)

@dp.message(F.text == "Да" or F.text == "Личный кабинет")
async def start_quiz(message: Message):
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer("Сначала нажми /start")
        return
    total_done = user['correct_answers'] + user['incorrect_answers']
    if total_done > 0:
        winrate = f"🎯 Винрейт: <b>{round(user['correct_answers'] / total_done*100)}</b>\n\n"
    else:
        winrate = f"🎯 Винрейт: <b>Вы не сделали ещё ни 1 задачи!</b>\n\n"

    rank = await get_user_rank(message.from_user.id)
    total_users = await get_total_users()
    created = user['created_at'][:16] if user['created_at'] else "-"
    await message.answer(
        f"👤 <b>Личный кабинет</b>\n\n"
        f"Имя: <b>{user['full_name']}</b>\n"
        f"📅 С нами с: {created}\n\n"
        f"📊 <b>Статистика</b>\n"
        f"💼Всего задач: <b>{total_done}</b>\n"
        f"✅ Правильных: <b>{user['correct_answers']}</b>\n"
        f"❌ Неправильных: <b>{user['incorrect_answers']}</b>\n"
        f"{winrate}"
        f"🏆 Место в топе: <b>{rank}</b> из {total_users}",
        parse_mode="HTML")
async def main():
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
