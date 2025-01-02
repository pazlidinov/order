import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db_customer, bot
from keyboards.default.balance_key import balance_btn


def update_balance(message):
    args = message.get_args()
    inviter_id = int(args) if args.isdigit() else None

    if inviter_id:
        try:
            db_customer.update_customer(
                id=inviter_id,
                invited=1,
                balance=50,
            )
        except Exception as err:
            logging.exception(err)


def add_user(message, bot_username):
    id = message.from_user.id
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    # Referal havola yaratish
    offer_link = f"https://t.me/{bot_username}?start={id}"

    try:
        db_customer.add_customer(
            id=int(id),
            name=name,
            last_name=last_name,
            username=username,
            offer_link=offer_link,
            invited=0,
            balance=0,
        )
        update_balance(message)
    except Exception as err:
        logging.exception(err)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = db_customer.select_customer(id=message.from_user.id)
    if not user:
        bot_username = (await bot.get_me()).username
        add_user(message, bot_username)
    await message.answer(
        f"Salom, {message.from_user.full_name}!\nBu bot orqali ijtimoiytarmoqlardan videolarni yuklab olishingiz mumkin.",
        reply_markup=balance_btn,
    )
