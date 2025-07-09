from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    task = State()
    category = State()