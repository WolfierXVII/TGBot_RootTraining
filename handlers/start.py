from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database import add_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(
        telegram_id = message.from_user.id,
        full_name = message.from_user.full_name
    )
    await message.answer(f"Приветствую тебя, {message.from_user.full_name}!\n"
                        f"При помощи данного бота ты сможешь обучиться считать приближённые корни чисел!\n"
                        f"Тебе доступны следующие команды:\n"
                        f"/cabinet — 👤 Личный кабинет\n"
                        f"/learn — 📚 Обучение \n"
                        f"/tasks — ▶️ Практика \n"
                        f"/top — 🏆 Топ игроков\n"
                        f"/help — ❓ Справка",
                        parse_mode = "HTML"
                        )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "❓ <b>Справка</b>\n\n"
        "Этот бот учит считать приближённые корни чисел "
        "с помощью вавилонского метода.\n\n"
        "📋 <b>Команды:</b>\n"
        "/start — запустить бота\n"
        "/cabinet — личный кабинет и статистика\n"
        "/learn — пошаговое обучение методу\n"
        "/tasks — решать задачи\n"
        "/top — топ игроков\n"
        "/help — эта справка",
        parse_mode = "HTML"
    )