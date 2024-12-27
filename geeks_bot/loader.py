from data import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.table_customer import DatabaseCustomer
from utils.db_api.table_course import DatabaseCourse
from utils.db_api.table_registration import DatabaseRegistration


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_customer = DatabaseCustomer(path_to_db="training_center/db.sqlite3")
db_course = DatabaseCourse(path_to_db="training_center/db.sqlite3")
db_registration = DatabaseRegistration(path_to_db="training_center/db.sqlite3")
