import datetime
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from loader import dp, bot, db_course, db_customer
from keyboards.default.menu import menu_btn
from keyboards.inline.callback_data import course_callback
from data.config import ADMINS
import logging


@dp.message_handler(Text("Markza haqida"))
async def about_center(message: types.Message):
    await message.answer(
        "GEEKS\n\nZamonaviy kasblar orqali pul topishni o’rganamiz!\n\nManzilimiz:<a href='https://maps.google.com/maps?q=40.752825,72.346648'>  Lermontova 14, Andijan 170103</a>\nInstagram:<a href='https://www.instagram.com/geeks.andijan?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=='>  geeks.andijan</a>"
    )


@dp.message_handler(Text("Kurslarimiz"))
async def all_courses(message: types.Message):
    course_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    courses = [course[1] for course in db_course.select_all_course()]
    if len(courses) % 2 == 0:
        for i in range(0, len(courses), 2):
            course_btn.row(
                KeyboardButton(text=courses[i]), KeyboardButton(text=courses[i + 1])
            )
        course_btn.add(KeyboardButton(text="Orqaga"))
    else:
        courses.append("Orqaga")
        for i in range(0, len(courses), 2):
            course_btn.row(
                KeyboardButton(text=courses[i]), KeyboardButton(text=courses[i + 1])
            )

    await message.answer(
        "Yo'nalishlarda mavjud kurslarni ko'rish uchun quyidagi bo'limlardan birini tanlang.",
        reply_markup=course_btn,
    )


@dp.message_handler(Text("Orqaga"))
async def back(message: types.Message):
    await message.answer(
        "Quyidagi tugmalar orqali o'zingizga kerakli bo'limni tanlang.",
        reply_markup=menu_btn,
    )


@dp.message_handler(state=None)
async def one_course(message: types.Message):
    info_course = db_course.select_course(name=message.text)
    register_to_course = InlineKeyboardMarkup(row_width=1)
    register_to_course.insert(
        InlineKeyboardButton(
            text="Ro'yhatdan o'tish",
            callback_data=course_callback.new(item_name=info_course[0]),
        )
    )
    await message.answer(
        f"Kurs nomi: {info_course[1]}\nHaftada: {info_course[2]} kun\nDars soati: {info_course[-1]}\nKurs narxi: {info_course[4]} so'm\nChegirma: {info_course[5]} %\nKurs davomida siz:\n{info_course[6]}",
        reply_markup=register_to_course,
    )


@dp.callback_query_handler(text_contains="course")
async def register_to_course(call: types.CallbackQuery):
    course = db_course.select_course(id=call.data[-1])
    customer = db_customer.select_user(id=call.from_user.id)

    msg = "Kurs uchun ro'yhatdan o'tildi:\n"
    msg += f"Username - <a href='https://t.me/{customer[3]}'>{customer[3]}</a>\n"
    msg += f"Ismi - {customer[1]}\n"
    msg += f"Familyasi - {customer[2]}\n"
    msg += f"Telefon raqami - {customer[4]}\n"
    msg += f"Kurs - {course[1]}"


    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text=msg)
            # await bot.answer_callback_query(admin, msg, cache_time=60)
        except Exception as err:
            logging.exception(err)

    await call.answer("Siz kursga yozildingiz", cache_time=60, show_alert=True)
