from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_user, get_user_rank, get_total_users

router = Router()

async def build_cabinet_text(telegram_id: int) -> str | None:
    user = await get_user(telegram_id)
    if user is None:
        return None
    total_done = user['correct_answers'] + user['incorrect_answers']
    if total_done > 0:
        winrate = f"🎯 Винрейт: <b>{round(user['correct_answers'] / total_done*100)}%</b>\n\n"
    else:
        winrate = f"🎯 Винрейт: <b>Вы не сделали ещё ни 1 задачи!</b>\n\n"
      
    rank = await get_user_rank(telegram_id)
    total_users = await get_total_users()
    created = user['created_at'][:16] if user['created_at'] else "-"
    return(
            f"👤 <b>Личный кабинет</b>\n\n"
            f"Имя: <b>{user['full_name']}</b>\n"
            f"📅 С нами с: {created}\n\n"
            f"📊 <b>Статистика</b>\n"
            f"💼 Всего задач: <b>{total_done}</b>\n"
            f"✅ Правильных: <b>{user['correct_answers']}</b>\n"
            f"❌ Неправильных: <b>{user['incorrect_answers']}</b>\n"
            f"{winrate}"
            f"🏆 Место в топе: <b>{rank}</b> из {total_users}")
      


@router.message(Command("cabinet"))
async def cabinet(message: Message):
    text = await build_cabinet_text(message.from_user.id)
    if text is None:
        await message.answer("Сначала нажми /start")
        return
    await message.answer(text, parse_mode="HTML")

