from aiogram import types
from aiogram.types import InlineKeyboardButton


def keyboard_category():
    kb = [
        [InlineKeyboardButton(text='Да', callback_data='yes_category')],
        [InlineKeyboardButton(text='Нет', callback_data='no_category')],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def menu_keyboard():
    kb = [
        [InlineKeyboardButton(text='Профиль', callback_data='profile')],
        [InlineKeyboardButton(text='Мои задачи', callback_data='my_tasks')],
        [InlineKeyboardButton(text='Добавить задачу', callback_data='add_task_kb')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def start_keyboard():
    kb = [
        [InlineKeyboardButton(text='Меню', callback_data='menu_kb')],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)
