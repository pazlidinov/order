import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


from loader import dp, bot
from states.studentData import StudentData
from data.config import ADMINS
from keyboards.default.contact import contact_btn


@dp.message_handler(Command("student"), chat_id=ADMINS)
async def username_stage(message: types.Message):
    await message.answer("Siz admin sifatida ro'yhatdan o'tkazilgansiz.")


@dp.message_handler(Command("student"))
async def username_stage(message: types.Message):
    await message.answer("Ismingizni kiriting...")
    await StudentData.name.set()


@dp.message_handler(state=StudentData.name)
async def name_stage(message: types.Message, state: FSMContext):
    username = message.from_user.username
    name = message.text

    await state.update_data({"username": username})
    await state.update_data({"name": name})
    await message.answer("Familyangizni kirirting...")
    await StudentData.next()


@dp.message_handler(state=StudentData.surname)
async def name_stage(message: types.Message, state: FSMContext):
    surname = message.text

    await state.update_data({"surname": surname})
    await message.answer("Telefon raqamingizni kirirting...", reply_markup=contact_btn)
    await StudentData.next()


@dp.message_handler(
    content_types="contact", is_sender_contact=True, state=StudentData.phonenumber
)
async def name_stage(message: types.Message, state: FSMContext):
    phonenumber = message.contact

    await state.update_data({"phonenumber": phonenumber.phone_number})
    await message.answer("Ta'lim yo'nalishingizni kirirting...")
    await StudentData.next()


@dp.message_handler(state=StudentData.direction)
async def name_stage(message: types.Message, state: FSMContext):

    direction = message.text

    await state.update_data({"direction": direction})
    await message.answer("Guruhingizni kirirting...")
    await StudentData.next()


@dp.message_handler(state=StudentData.group)
async def name_stage(message: types.Message, state: FSMContext):
    group = message.text

    await state.update_data({"group": group})
    await message.answer("O'qituvchingizni ism, familyasini kirirting...")
    await StudentData.next()


@dp.message_handler(state=StudentData.teacher)
async def name_stage(message: types.Message, state: FSMContext):
    teacher = message.text

    await state.update_data({"teacher": teacher})
    await message.answer("Murojaatingizni yuboring...")
    await StudentData.next()


@dp.message_handler(state=StudentData.text)
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
    direction = data.get("direction")
    group = data.get("group")
    teacher = data.get("teacher")
    body_text = data.get("text")

    # New reference text
    msg = "Sizga yangi murojaat qoldirildi:\n"
    msg += f"Username - <a href='https://t.me/{username}'>{username}</a>\n"
    msg += f"Ismi - {name}\n"
    msg += f"Familyasi - {surname}\n"
    msg += f"Telefon raqami - {phonenumber}\n"
    msg += f"Ta'lim yo'nalishi - {direction}\n"
    msg += f"Guruhi - {group}\n"
    msg += f"O'qituvchi - {teacher}\n"
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
