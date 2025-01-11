from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from utils.db_api.table_customer import DatabaseCustomer
from utils.db_api.table_inviteamount import DatabaseInviteAmount


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_customer = DatabaseCustomer(path_to_db="web/db.sqlite3")
db_inviteamount = DatabaseInviteAmount(path_to_db="web/db.sqlite3")
