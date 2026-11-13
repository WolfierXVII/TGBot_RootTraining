import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

import src_private
from database import init_db

from handlers import start, cabinet, learn, tasks, top 

logging.basicConfig(level = logging.INFO)

bot = Bot(token = src_private.bot_token)
dp = Dispatcher()


async def main():
    await init_db()

    dp.include_router(start.router)
    dp.include_router(cabinet.router)
    dp.include_router(learn.router)
    dp.include_router(tasks.router)
    dp.include_router(top.router)
    
    await bot.set_my_commands([
        BotCommand(command="start",   description="🚀 Запустить бота"),
        BotCommand(command="help",    description="❓ Справка"),
        BotCommand(command="cabinet", description="👤 Личный кабинет"),
        BotCommand(command="learn",   description="📚 Обучение"),
        BotCommand(command="tasks",   description="▶️ Практика (задачи)"),
        BotCommand(command="top",     description="🏆 Топ игроков"),
    ])
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())