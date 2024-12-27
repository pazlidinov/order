import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart

API_TOKEN = (
    "7664329456:AAGD4ikJ9jvmkAb1zff870idz3wHb2BKHo0"  # Введите токен вашего бота
)
CHANNEL_USERNAME = "@cantssilent"  # Имя пользователя канала

# Настройки журналирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):    
    await message.answer(f"Привет, {message.from_user.full_name}! Через этого бота вы можете анонимно комментировать посты на канале Can'tSilent.")


@dp.message_handler()
async def handle_message(message: types.Message):
    # Принятие сообщения, отправленного боту
    
    last_post = await bot.get_chat(CHANNEL_USERNAME)  # Получить информацию о канале
    # logging.info(f"ID последнего поста, опубликованного на канале: {last_post.id}")

    # Комментарий на канале
    await bot.send_message(
        CHANNEL_USERNAME,
        f"Комментарий: {message.text}",
        reply_to_message_id=last_post.id,
    )

    await message.reply("Ваш комментарий добавлен на канал!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
