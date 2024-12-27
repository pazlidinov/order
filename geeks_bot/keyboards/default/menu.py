from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Markza haqida"),
            KeyboardButton(text="Kurslarimiz"),
        ],
    ],
    resize_keyboard=True,
)

