from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user_keyboards import keyboard_category
from bot.states.user_states import User

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я - твой помощник для управления задачами. '
                         'Я помогу создавать, отслеживать и напоминать о важных делах!\n\n'
                         'Не знаешь, с чего начать? Напиши /help — '
                         'я расскажу о всех моих функциях и командах!')

@user_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Пропиши /add чтобы добавить новую задачу')

@user_router.message(Command('add'))
async def add_task(message: Message, state: FSMContext):
    await state.set_state(User.task)
    await message.answer('Введите вашу задачу, например, "Купить молоко"')

@user_router.message(User.task)
async def add_category(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    await message.answer('Хотите добавить категорию?', reply_markup=keyboard_category())

@user_router.callback_query(F.data.in_(['yes_category', 'no_category']))
async def set_category(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes_category':
        await state.set_state(User.category)
        await call.message.edit_text('Введите новую категорию')

@user_router.message(User.category)
async def complete_add(message: Message, state: FSMContext):
    await state.update_data(categoty=message.text)
    data = await state.get_data()
    await message.answer(f'{data}')

