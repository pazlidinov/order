import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot

from data.config import ADMINS


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
    for admin in ADMINS:
        try:
            await bot.send_message(
                admin, "Siz admin sifatida ro'yhatdan o'tkazilgansiz."
            )
        except Exception as err:
            logging.exception(err)
