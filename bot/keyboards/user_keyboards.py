from aiogram import types
from aiogram.types import InlineKeyboardButton


def keyboard_category():
    kb = [
        [InlineKeyboardButton(text='Да', callback_data='yes_category')],
        [InlineKeyboardButton(text='Нет', callback_data='no_category')],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)