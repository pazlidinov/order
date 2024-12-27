from aiogram import Bot, Dispatcher, executor, types
import logging
import requests

API_TOKEN = "5144558662:AAGQ5-HnVVtu9YslIt-HNcNzO5X2ZT8ky4c"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    welcome_text = "Assalomu alaykum, botga xush kelibsiz!\n\n"
    await message.answer(welcome_text)


# Yangi foydalanuvchi botga qo'shilganda xabar yuborish
@dp.message_handler()
async def handle_new_user(message: types.Message):
    # URL ga GET so'rovi yuborish
    response = requests.get("https://cr.minzdrav.gov.ru/clin_recomend")
    print(response.content)
    # Javobni ekranga chiqarish
    # print(response.text)  # Yoki response.json() JSON formatda bo'lsa
    await message.reply(response.content)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
