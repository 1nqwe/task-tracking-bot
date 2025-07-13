from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    newsletter = State()