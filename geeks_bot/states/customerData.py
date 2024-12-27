from aiogram.dispatcher.filters.state import State, StatesGroup


class Customer(StatesGroup):
    name = State()
    surname = State()
    phonenumber = State()
   