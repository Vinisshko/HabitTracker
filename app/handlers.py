from email import message
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from app.database.requests import get_user_habits
from app.keyboards import create_habits_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.database.requests import remove_habit, mark_habit_as_completed, get_habit_statistics, mark_habit_as_not_completed
from sqlalchemy.ext.asyncio import async_session
from app.database.models import HabitModel

import app.keyboards as kb
import app.database.requests as rg



storage = MemoryStorage()
router = Router()

class Register(StatesGroup):
    name = State()
    #age = State()

class HabitStates(StatesGroup):
    set_habit = State()
    
    

@router.message(CommandStart())  # декоратор(обработка сообщений)
async def cmd_start(message: Message):  # ловим сообщения
    await rg.set_user(message.from_user.id)
    await message.answer(
    """Привет! 👋 
Добро пожаловать в нашего помощника по созданию привычек! 🌱
Здесь ты сможешь легко установить и отслеживать свои привычки, получать напоминания и вдохновение для достижения целей. 
Готов начать свой путь к лучшей версии себя?
Давай сделаем это вместе! 💪✨""", reply_markup=kb.main
    )  # ответ пользователю



@router.message(Command("help"))
async def cmd_help(message: Message):   #параметр, в который приходит сообщение из декоратора
    await message.answer("Вы нажали на кнопку помощи")



@router.message(F.text == "Привычки")  # мини диалог
async def habit(message: Message):
    user_id = message.from_user.id 
    user_habits = await get_user_habits(user_id)  # Получаем привычки пользователя
    #await message.answer("Выберите привычку", reply_markup=kb.habit)
    
    #if user_habits:
       #habits_keyboard = create_habits_keyboard(user_habits)
        #await message.answer("Ваши привычки:", reply_markup=habits_keyboard)
    #else:
        #await message.answer("У вас нет активных привычек.", reply_markup=add_habit_keyboard())
        
        
    try:
        user_habits = await get_user_habits(user_id)
        if user_habits: 
           habits_keyboard = create_habits_keyboard(user_habits) 
           await message.answer("Ваши привычки:", reply_markup=habits_keyboard) 
        else: 
           await message.answer("У вас нет активных привычек.", reply_markup=create_habits_keyboard([]))
    except Exception as e:
       print(f"Ошибка при получении привычек: {e}")
       await message.answer("Произошла ошибка при получении ваших привычек.")    
    

@router.callback_query(F.data == ("add"))
async def add_habit(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Введите название привычки: ")
    await state.set_state(HabitStates.set_habit)  # Устанавливаем состояние
      
# Ожидание ответа пользователя
@router.message(HabitStates.set_habit)
async def set_habit(message: Message, state: FSMContext):
    habit_name = message.text  # Получаем текст из сообщения
    user_id = message.from_user.id  # Получаем ID пользователя
    #await save_habit(habit_name, user_id)  # Передаем user_id в функцию сохранения привычки
    await rg.save_habit(habit_name, user_id)
    await message.answer(f"Привычка {habit_name} добавлена!\n")
    await state.clear()
   
    user_habits = await get_user_habits(user_id)
    habits_keyboard = create_habits_keyboard(user_habits)
    await message.answer("Ваши привычки:", reply_markup=habits_keyboard)
    
    await state.clear()


@router.callback_query(F.data.startswith("habit_")) 
async def handle_habit(callback: CallbackQuery): 
    habit_id = callback.data.split("_")[1] 
    
    # Создаем клавиатуру с кнопками "Удалить" и "Просмотреть статистику"
    habit_keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [ 
            InlineKeyboardButton(text="Удалить", callback_data=f"confirm_delete_{habit_id}"), 
            InlineKeyboardButton(text="Просмотреть статистику", callback_data=f"view_stats_{habit_id}") 
        ] 
    ]) 
    
    await callback.message.answer("Выберите действие:", reply_markup=habit_keyboard)

@router.callback_query(F.data.startswith("confirm_delete_")) 
async def confirm_delete_habit(callback: CallbackQuery): 
    habit_id = callback.data.split("_")[2] 
    
    # Создаем клавиатуру для подтверждения удаления 
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [ 
            InlineKeyboardButton(text="Да, удалить", callback_data=f"delete_{habit_id}"), 
            InlineKeyboardButton(text="Нет, отменить", callback_data="cancel_delete") 
        ] 
    ]) 
    
    await callback.message.answer("Вы уверены, что хотите удалить эту привычку?", reply_markup=confirm_keyboard)

@router.callback_query(F.data.startswith("delete_")) 
async def delete_habit(callback: CallbackQuery): 
    habit_id = callback.data.split("_")[1] 
    user_id = callback.from_user.id 

    # Удаляем привычку из базы данных 
    await rg.remove_habit(habit_id, user_id) 

    await callback.answer("Привычка удалена!") 
    
    # Обновляем список привычек после удаления 
    user_habits = await get_user_habits(user_id) 
    habits_keyboard = create_habits_keyboard(user_habits) 
    await callback.message.answer("Ваши привычки:", reply_markup=habits_keyboard) 

@router.callback_query(F.data == "cancel_delete") 
async def cancel_delete(callback: CallbackQuery): 
    await callback.answer("Удаление отменено.")

@router.callback_query(F.data.startswith("view_stats_")) 
async def view_stats(callback: CallbackQuery):
    habit_id = callback.data.split("_")[2]
    
    # Логика получения статистики по привычке
    stats = await get_habit_statistics(habit_id)
    
    await callback.message.answer(f"Статистика по привычке {habit_id}: {stats}")
    
    
@router.message(F.text == "Состояние привычек")  # мини диалог
async def statushabit(message: Message):
    await message.answer("Выберите привычку", reply_markup=kb.habit)

@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\n')
    #await state.set_state(Register.age)
    #await message.answer('Введите ваш возраст')
    await state.clear()
    
    
#@router.message(Register.age)
#async def register_name_handler(message: Message, state: FSMContext):
    #await state.update_data(age=message.text)
    #data = await state.get_data()

    #await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data['age']}')
    #await state.clear()
    
    
@router.message(Command("show_habits")) #это декоратор, который указывает, что данная функция будет вызываться при получении сообщения с командой "/show_habits"
async def show_habits(message: Message): # функция, которая отвечает за отображение списка привычек пользователя.
    user_id = message.from_user.id
    habits = await get_user_habits(user_id)

    # Проверка, есть ли привычки у пользователя
    if not habits:
        await message.answer("У Вас нет привычек.")
        return

    keyboard = InlineKeyboardMarkup(row_width=3)  # Теперь 3 кнопки в ряд

    for habit in habits:
        button_done = InlineKeyboardButton("✅", callback_data=f"mark_done_{habit.Habitid}")
        button_not_done = InlineKeyboardButton("❌", callback_data=f"mark_not_done_{habit.Habitid}")
        row = [ #создание списка, который будет содержать несколько кнопок
            InlineKeyboardButton(habit.Habit_name, callback_data=f"view_stats_{habit.Habitid}"),
            button_done,
            button_not_done
        ]
        keyboard.add(*row)
    
    await message.answer("Ваши привычки:", reply_markup=keyboard)
    
    
    
    
@router.callback_query(F.data.startswith("mark_done_"))
async def mark_done(callback: CallbackQuery):
    habit_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    async with async_session() as session:
        await mark_habit_as_completed(habit_id, user_id, session)

    await callback.answer("Привычка отмечена как выполненная!")
    await show_habits(callback.message)
    
@router.callback_query(F.data.startswith("mark_not_done_"))
async def mark_not_done(callback: CallbackQuery):
    habit_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    async with async_session() as session:
        await mark_habit_as_not_completed(habit_id, user_id, session)

    await callback.answer("Привычка отмечена как не выполненная!")
    await show_habits(callback.message)
    
    
@router.message(Command("stats"))
async def show_statistics(message: Message):
    user_id = message.from_user.id
    habits = await get_habit_statistics(user_id)

    response = "Статистика привычек:\n"
    for habit in habits: 
        last_completed = habit.last_completed_date.strftime("%Y-%m-%d") if habit.last_completed_date else "Не выполнена"
        response += f"{habit.Habit_name}: {habit.completed_streak} дней подряд, Последнее выполнение: {last_completed}\n" 

    await message.answer(response)
    
    
    
@router.callback_query(F.data.startswith("view_stats_"))  
async def view_stats(callback: CallbackQuery): 
    habit_id = callback.data.split("_")[2] 
    stats = await get_habit_statistics(habit_id) 
    
    if stats:
        await callback.message.answer(f"Статистика по привычке {stats['name']}: {stats['completed_streak']} дней подряд, Последнее выполнение: {stats['last_completed_date']}")
    else:
        await callback.message.answer("Привычка не найдена.")
           