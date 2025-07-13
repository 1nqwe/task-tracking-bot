from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_kb():
    kb = [
        [InlineKeyboardButton(text='Админ-Панель', callback_data='admin_menu')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def admin_keyboard():
    kb = [
        [
            InlineKeyboardButton(text='Рассылка', callback_data='admin_newsletter'),
            InlineKeyboardButton(text='Статистика', callback_data='admin_statistic')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def back_admin_menu_kb():
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data='admin_menu')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)