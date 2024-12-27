from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from keyboards.default.course import course_btn


import logging

@dp.message_handler(Text('Markza haqida'))
async def bot_start(message: types.Message):
    await message.answer("GEEKS\nBiz bilan zamonaviy kasblarni zamonaviy kasblarni o'rganing.\n\nManzilimiz:<a href='https://maps.google.com/maps?q=40.752825,72.346648'>  Lermontova 14, Andijan 170103</a>\nInstagram:<a href='https://www.instagram.com/geeks.andijan?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=='>  geeks.andijan</a>")
    
@dp.message_handler(Text('Kurslarimiz'))
async def bot_start(message: types.Message):    
    await message.answer("Yo'nalishlarda mavjud kurslarni ko'rish uchun quyidagi bo'limlardan birini tanlang.", reply_markup=course_btn)