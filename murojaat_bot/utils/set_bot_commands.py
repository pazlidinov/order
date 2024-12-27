from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("general", "Umumiy tartibda murojaat yo'llash"),
            types.BotCommand("student", "O'quvchilar tartibida murojaat yo'llash"),
        ]
    )
