from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.database import complete_add_task
from bot.keyboards.user_keyboards import keyboard_category, menu_keyboard, start_keyboard
from bot.states.user_states import User

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я - твой помощник для управления задачами. '
                         'Я помогу создавать, отслеживать и напоминать о важных делах!\n\n'
                         'Не знаешь, с чего начать? Напиши /help — '
                         'я расскажу о всех моих функциях и командах!', reply_markup=start_keyboard())

@user_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Пропиши /add чтобы добавить новую задачу')

@user_router.callback_query(F.data == 'add_task_kb')
async def add_task(call: CallbackQuery, state: FSMContext):
    await state.set_state(User.task)
    await call.message.edit_text('Введите вашу задачу, например, "Купить молоко"')

@user_router.message(User.task)
async def add_category(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    await message.answer('Хотите добавить категорию?', reply_markup=keyboard_category())

@user_router.callback_query(F.data.in_(['yes_category', 'no_category']))
async def set_category(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes_category':
        await state.set_state(User.category)
        await call.message.edit_text('Введите новую категорию')
    else:
        data = await state.get_data()
        try:
            await complete_add_task(
                user_id=call.message.from_user.id,
                task=data['task'],
            )
            await call.message.edit_text('Данные успешно добавлены!')
        except:
            await call.message.edit_text(f'Ошибка при сохранении')
        finally:
            await state.clear()


@user_router.message(User.category)
async def complete_add(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()
    try:
        await complete_add_task(
            user_id=message.from_user.id,
            task=data['task'],
            category=data['category']
        )
        await message.answer('Данные успешно добавлены!')
    except:
        await message.answer(f'Ошибка при сохранении')
    finally:
        await state.clear()

@user_router.callback_query(F.data == 'menu_kb')
async def user_menu(call: CallbackQuery):
    await call.message.edit_text('Меню:', reply_markup=menu_keyboard())