import asyncio

from aiogram import Router, F, types
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, TelegramObject

from bot.database.database import get_user_count, get_all_users_id
from bot.keyboards.admin_keyboards import admin_keyboard, admin_menu_kb, back_admin_menu_kb
from bot.states.admin_states import AdminState
from config import ADMINS


class IsAdmin(BaseFilter):
    async def __call__(self, obj: TelegramObject):
        return obj.from_user.id in ADMINS

admin_router = Router()

@admin_router.message(Command('admin'), IsAdmin())
async def cmd_admin(message: Message):
    await message.answer('Добро пожаловать в админ панель', reply_markup=admin_menu_kb())

@admin_router.callback_query(F.data == 'admin_menu', IsAdmin())
async def admin_menu(call: CallbackQuery):
    await call.message.edit_text('Админ-Панель', reply_markup=admin_keyboard())

@admin_router.callback_query(F.data == 'admin_statistic', IsAdmin())
async def admin_statistic(call: types.CallbackQuery):
    user_count = await get_user_count()
    await call.message.edit_text('Статистика\n\n'
                                 f'Количество пользователей: {user_count}', reply_markup=back_admin_menu_kb())


@admin_router.callback_query(F.data == 'admin_newsletter')
async def admin_newsletter(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.newsletter)
    await call.message.edit_text('Введите текст')

@admin_router.message(AdminState.newsletter)
async def admin_newsletter_step_2(message: Message, state: FSMContext):
    all_ids = await get_all_users_id()
    for user_id in all_ids:
        await asyncio.sleep(0.3)
        await message.send_copy(user_id[0])
    await state.clear()