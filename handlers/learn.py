# handlers/learn.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from theory import THEORY
from keyboards import theory_keyboard
from database import set_learned

router = Router()


@router.message(Command("learn"))
async def cmd_learn(message: Message):
    step=0
    t = THEORY[step]
    await message.answer(
        f"<b>{t['title']}</b>\n\n{t['text']}",
        reply_markup=theory_keyboard(step, len(THEORY)),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("theory:"))
async def theory_step(callback: CallbackQuery):
    step = int(callback.data.split(":")[1])
    step = max(0,min(step, len(THEORY) - 1))
    t = THEORY[step]

    if step == len(THEORY) - 1:
        await set_learned(callback.from_user.id)
        
    await callback.message.edit_text(
                f"<b>{t['title']}</b>\n\n{t['text']}",
                reply_markup=theory_keyboard(step,len(THEORY)),
                parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "to_menu")
async def to_menu(callback: CallbackQuery):
    await callback.message.answer(
         "🏠 Ты в меню. Используй команды:\n"
        "/cabinet — личный кабинет\n"
        "/tasks — практика\n"
        "/top — топ игроков\n"
        "/learn — повторить теорию"
    )
    await callback.answer()