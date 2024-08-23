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


habit = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить привычку", callback_data="add")],
        [InlineKeyboardButton(text="Удалить привычку", callback_data="del")],
    ]
)


statushabit = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить привычку", callback_data="add")],
        [InlineKeyboardButton(text="Удалить привычку", callback_data="del")],
    ]
)
