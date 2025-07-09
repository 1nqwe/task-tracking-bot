from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


def my_task_keyboard(tasks):
    builder = InlineKeyboardBuilder()

    for task_id, task_text in tasks:
        builder.button(
            text=f"{task_text[:15]}...",
            callback_data=f"task_{task_id}"
        )
    builder.button(text="Назад",
                    callback_data="menu_kb")
    builder.adjust(1)
    return builder.as_markup()

def back_to_tasks_keyboard():
    kb = [
        [InlineKeyboardButton(text='Назад к списку', callback_data='my_tasks')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def back_to_menu():
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data='menu_kb')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)