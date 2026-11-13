# handlers/learn.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("learn"))
async def cmd_learn(message: Message):
    await message.answer("📚 Обучение скоро появится!")