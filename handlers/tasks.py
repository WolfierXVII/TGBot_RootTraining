# handlers/tasks.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    await message.answer("▶️ Задачи скоро появятся!")