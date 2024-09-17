from app.database.models import HabitModel
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привычки"), KeyboardButton(text="Состояние привычек")],
        [KeyboardButton(text="Мои задачи"), KeyboardButton(text="Состояние задач")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...",
)



def create_habits_keyboard(habits):
    # Создаем список для кнопок
    buttons = []
    
    for habit in habits:
        button = InlineKeyboardButton(text=habit.Habit_name, callback_data=f"habit_{habit.Habitid}")
        buttons.append([button])  # Каждая кнопка в своем ряду

# Добавляем дополнительные кнопки
    buttons.append([InlineKeyboardButton(text="➕", callback_data="add")])

    # Создаем клавиатуру с правильной структурой
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    return keyboard

# Кнопка для добавления привычки
def add_habit_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Добавить привычку", callback_data="add")
    keyboard.add(button)
    return keyboard

#Создаем клавиатуру для подтверждения удаления
    #confirm_keyboard = InlineKeyboardMarkup()
    #confirm_button = InlineKeyboardButton(text="Удалить", callback_data=f"delete_{habit_id}")
    #cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel_delete")
    
    #confirm_keyboard.add(confirm_button, cancel_button)
    
    
#habit = InlineKeyboardMarkup(
    #inline_keyboard=[
        #[InlineKeyboardButton(text="Добавить привычку", callback_data="add")],
        #[InlineKeyboardButton(text="Удалить привычку", callback_data="del")],
    #]
#)


statushabit = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить привычку", callback_data="add")],
        [InlineKeyboardButton(text="Удалить привычку", callback_data="del")],
    ]
)



def create_habit_buttons(habit_id):
    keyboard = InlineKeyboardMarkup()
    keyboard = (InlineKeyboardButton("Выполнено", callback_data=f"mark_done_{habit_id}"))
    keyboard = (InlineKeyboardButton("Не выполнено", callback_data=f"mark_not_done_{habit_id}"))
    return keyboard