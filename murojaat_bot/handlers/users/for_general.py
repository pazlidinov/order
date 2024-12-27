import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


from loader import dp, bot
from states.generalData import GeneralData
from data.config import ADMINS
from keyboards.default.contact import contact_btn


@dp.message_handler(Command("general"), chat_id=ADMINS)
async def username_stage(message: types.Message):
    await message.answer("Siz admin sifatida ro'yhatdan o'tkazilgansiz.")


@dp.message_handler(Command("general"))
async def username_stage(message: types.Message):
    await message.answer("Ismingizni kiriting...")
    await GeneralData.name.set()


@dp.message_handler(state=GeneralData.name)
async def name_stage(message: types.Message, state: FSMContext):
    username = message.from_user.username
    name = message.text

    await state.update_data({"username": username})
    await state.update_data({"name": name})
    await message.answer("Familyangizni kirirting...")
    await GeneralData.next()


@dp.message_handler(state=GeneralData.surname)
async def name_stage(message: types.Message, state: FSMContext):
    surname = message.text

    await state.update_data({"surname": surname})
    await message.answer("Telefon raqamingizni kirirting...", reply_markup=contact_btn)
    await GeneralData.next()


@dp.message_handler(
    content_types="contact", is_sender_contact=True, state=GeneralData.phonenumber
)
async def name_stage(message: types.Message, state: FSMContext):
    phonenumber = message.contact

    await state.update_data({"phonenumber": phonenumber.phone_number})
    await message.answer("Murojaatingizni yuboring...")
    await GeneralData.next()


@dp.message_handler(state=GeneralData.text)
async def name_stage(
    message: types.Message,
    state: FSMContext,
):

    text = message.text

    await state.update_data({"text": text})

    # Read data again
    data = await state.get_data()
    username = data.get("username")
    name = data.get("name")
    surname = data.get("surname")
    phonenumber = data.get("phonenumber")
    body_text = data.get("text")

    # New reference text
    msg = "Sizga yangi murojaat qoldirildi:\n"
    msg += f"Username - <a href='https://t.me/{username}'>{username}</a>\n"
    msg += f"Ismi - {name}\n"
    msg += f"Familyasi - {surname}\n"
    msg += f"Telefon raqami - {phonenumber}\n"
    msg += f"Murojaat matni - {body_text}\n"

    # send the appeal to the admins
    for admin in ADMINS:
        try:
            await bot.send_message(admin, msg)

        except Exception as err:
            logging.exception(err)

    await state.finish()
    await state.reset_state()
    await message.answer("Murojaatingiz adminga yuborildi.")
