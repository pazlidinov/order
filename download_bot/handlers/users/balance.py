from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp, bot, db_customer
from keyboards.default.balance_key import balance_btn


@dp.message_handler(Text("Hisob"))
async def show_balance(message: types.Message):
    user = db_customer.select_customer(id=message.from_user.id)
    await message.reply(
        f"Siz taklif qilganlar soni: {user[5]}\nSizning balansizngiz: {user[6]}\nSizning taklif havolangiz: {user[4]}"
    )
