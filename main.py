import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

import src_private
from database import init_db, add_user

bot = Bot(token=src_private.bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await add_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name
    )
    await message.answer(f"Приветствую тебя,{message.from_user.full_name}!\nПри помощи данного бота ты сможешь обучиться считать приближённые корни чисел!\nГотов начать?")

async def echo(message: types.Message):
    if message.text:
        await message.answer(message.text)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
