# handlers/top.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_top_users, get_user_rank, get_user

router = Router()


@router.message(Command("top"))
async def cmd_top(message: Message):
    top_users = await get_top_users(limit=10)

    if not top_users:
        await message.answer("🏆 Пока никого нет в топе. Начни решать задачи!")
        return
    
    lines = ["🏆 <b>Топ-10 игроков</b>\n"]
    for i, user in enumerate(top_users, start=1):
        places = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        name = user['full_name'] or "—"
        lines.append(f"{places} {name} — <b>{user['correct_answers']}</b> задач")

    my_rank = await get_user_rank(message.from_user.id)
    if my_rank and my_rank > 10:
        my_data= await get_user(message.from_user.id)
        name = my_data['full_name'] or "—"  
        lines.append(f"\n...")
        lines.append(f"{my_rank}. {name} — <b>{my_data['correct_answers']}</b> задач")

    await message.answer(
        "\n".join(lines), parse_mode="HTML"
    )