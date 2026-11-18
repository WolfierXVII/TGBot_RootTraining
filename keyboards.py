from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def theory_keyboard(step: int,total: int) -> InlineKeyboardMarkup:
    buttons = []

    row = []
    if step > 0:
        row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"theory:{step - 1}"))
    if step < total-1:
        row.append(InlineKeyboardButton(text="➡️ Дальше",callback_data=f"theory:{step + 1}"))
    if row:
        buttons.append(row)

    if step == total - 1:
        buttons.append([InlineKeyboardButton(text="🏠 В меню", callback_data="to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def tasks_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Получить задачу", callback_data="get_task")],
        [InlineKeyboardButton(text="👤 В личный кабинет", callback_data="to_cabinet")],
    ])
