import logging
from aiogram import types
from loader import dp, db_customer
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from states.customerData import Customer
from keyboards.default.contact import contact_btn
from keyboards.default.menu import menu_btn


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum! Iltimos, ismingizni kiriting...")
    await Customer.name.set()


@dp.message_handler(state=Customer.name)
async def name_stage(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    name = message.text

    await state.update_data({"user_id": user_id})
    await state.update_data({"username": username})
    await state.update_data({"name": name})
    await message.answer("Familyangizni kirirting...")
    await Customer.next()


@dp.message_handler(state=Customer.surname)
async def name_stage(message: types.Message, state: FSMContext):
    surname = message.text

    await state.update_data({"surname": surname})
    await message.answer("Telefon raqamingizni kirirting...", reply_markup=contact_btn)
    await Customer.next()


@dp.message_handler(
    content_types="contact", is_sender_contact=True, state=Customer.phonenumber
)
async def name_stage(message: types.Message, state: FSMContext):
    phonenumber = message.contact

    await state.update_data({"phonenumber": phonenumber.phone_number})

    # Ma'limotlarni qayta o'qish
    data = await state.get_data()
    user_id = data.get("user_id")
    username = data.get("username")
    name = data.get("name")
    surname = data.get("surname")
    phone = data.get("phonenumber")

    try:
        db_customer.add_customer(
            id=int(user_id), name=name, surname=surname, username=username, phone=phone
        )
    except Exception as err:
        logging.exception(err)       

    await message.answer(
        "Tabriklaymiz, muvaffaqiyatli ro'yxatdan o'tdingiz.\n Quyidagi tugmalar orqali o'zingizga kerakli bo'limni tanlang.",
        reply_markup=menu_btn,
    )
    await state.finish()
    await state.reset_state()
