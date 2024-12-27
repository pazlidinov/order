from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


course_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="course")],
    ],
    resize_keyboard=True,
)
