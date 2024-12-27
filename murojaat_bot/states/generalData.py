from aiogram.dispatcher.filters.state import State, StatesGroup


class GeneralData(StatesGroup):
    username = State()
    name = State()
    surname = State()
    phonenumber = State()
    text = State()
