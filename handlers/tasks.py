# handlers/tasks.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import is_learned

router = Router()


@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    if not await is_learned(message.from_user.id):
        await message.answer(
            "⚠️ Сначала пройди обучение!\n"
            "Для этого используй /learn"
        )
        return
    await message.answer("В разработке")