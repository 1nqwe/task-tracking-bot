from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.database import complete_add_task, add_user, count_user_tasks, get_all_user_tasks, get_task_info, \
    set_is_done, get_is_done, delete_task
from bot.keyboards.user_keyboards import keyboard_category, menu_keyboard, start_keyboard, my_task_keyboard, \
    task_keyboard, back_to_menu, back_task_menu, back_to_my_tasks
from bot.states.user_states import User

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
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
    await call.message.edit_text("📝 <b>Добавление новой задачи</b>\n"
                                "└ Введите текст, например: <i>Купить молоко</i>",
                                parse_mode="HTML", reply_markup=back_to_menu())

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
                user_id=call.from_user.id,
                task=data['task'],
            )
            await call.message.edit_text('Данные успешно добавлены!', reply_markup=back_to_menu())
        except:
            await call.message.edit_text(f'Ошибка при сохранении', reply_markup=back_to_menu())
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
        await message.answer('Данные успешно добавлены!', reply_markup=back_to_menu())
    except:
        await message.answer(f'Ошибка при сохранении', reply_markup=back_to_menu())
    finally:
        await state.clear()

@user_router.callback_query(F.data == 'menu_kb')
async def user_menu(call: CallbackQuery, state: FSMContext):
    if call.data == 'menu_kb':
        await state.clear()
    await call.message.edit_text('Меню:', reply_markup=menu_keyboard())

@user_router.callback_query(F.data == 'profile')
async def profile(call: CallbackQuery):
    await call.message.edit_text(f'Профиль:\n\n'
                                 f'👤<b>Ваше имя:</b> {call.from_user.full_name}\n'
                                 f'📊<b>Задач:</b> {await count_user_tasks(call.from_user.id)}',
                                 reply_markup=back_to_menu(), parse_mode="HTML")

@user_router.callback_query(F.data == 'my_tasks')
async def my_tasks(call: CallbackQuery):
    tasks = await get_all_user_tasks(call.from_user.id)
    await call.message.edit_text('Ваши задачи:', reply_markup=my_task_keyboard(tasks))

@user_router.callback_query(F.data.startswith("task_"))
async def task_info(call: CallbackQuery):
    task_id = call.data.split("_")[1]
    task = await get_task_info(task_id)
    task_text, category, is_done = task
    is_done = await get_is_done(task_id)
    message = (f'ID задачи #{task_id}\n\n'
               f'Текст: {task_text}\n'
               f'Категория: {category if category else "без категории"}\n'
               f'Статус: {'✅Выполнена' if (is_done == 1) else '❌Не выполнена'}')
    await call.message.edit_text(message, reply_markup=task_keyboard(task_id))

@user_router.callback_query(F.data.startswith("set_done_"))
async def set_done(call: CallbackQuery):
    task_id = call.data.split("_")[2]
    if await get_is_done(task_id) == 0:
        await set_is_done(1, task_id)
        await call.message.edit_text('Вы успешно поменяли статус:\n✅ Выполнено',
                                     reply_markup=back_task_menu(task_id))
    else:
        await set_is_done(0, task_id)
        await call.message.edit_text('Вы успешно поменяли статус:\n❌ Не выполнено',
                                     reply_markup=back_task_menu(task_id))

@user_router.callback_query(F.data.startswith("delete_task_"))
async def del_task(call: CallbackQuery):
    task_id = call.data.split("_")[2]
    await delete_task(task_id)
    await call.message.edit_text('Задача удалена', reply_markup=back_to_my_tasks())