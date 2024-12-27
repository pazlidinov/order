from aiogram.dispatcher.filters.state import State, StatesGroup


class StudentData(StatesGroup):
    username = State()
    name = State()
    surname = State()
    phonenumber = State()
    direction = State()
    group = State()
    teacher = State()
    text = State()
