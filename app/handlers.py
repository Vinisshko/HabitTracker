from email import message
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

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
    await message.answer("Выберите привычку", reply_markup=kb.habit)


@router.callback_query(F.data == ("add"))
async def add_habit(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Введите название привычки: ")
    await state.set_state(HabitStates.set_habit)  # Устанавливаем состояние
      
# Ожидание ответа пользователя
@router.message(HabitStates.set_habit)
async def set_habit(message: Message, state: FSMContext):
    habit_name = message.text  # Получаем текст из сообщения
    await rg.save_habit(habit_name)
    await message.answer(f"Привычка {habit_name} добавлена!\n")
    await state.clear()
   
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