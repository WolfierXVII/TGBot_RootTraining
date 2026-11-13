# handlers/top.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("top"))
async def cmd_top(message: Message):
    await message.answer("🏆 Топ скоро появится!")