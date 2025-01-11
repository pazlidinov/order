from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

balance_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Hisob"),
        ],
    ],
    resize_keyboard=True,
)
