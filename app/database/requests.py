from app.database.models import async_session
from app.database.models import User, HabitModel
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()
            
            
#async def set_habit(Habit_name):
    #async with async_session() as session:
        #Habit_name = await session.begin(session.add(Habit.Habit_name == Habit_name))
        
        #await session.commit()
        #(Habit.Habit_name == Habit_name))
       
async def get_user_habits(user_id: int):
    async with async_session() as session:
        habits = await session.execute(select(HabitModel).where(HabitModel.user_id == user_id))
        return habits.scalars().all()  # Возвращаем все привычки пользователя
       
async def save_habit(new_habit, user_id):        
    async with async_session() as session: 
        habit = HabitModel(Habit_name=new_habit, user_id=user_id)  # Создаем новый объект Habit 
        session.add(habit)  # Добавляем его в сессию 
        await session.commit()  # Сохраняем изменения в базе данных


async def remove_habit(habit_id: int, user_id: int):
    async with async_session() as session:
        # Находим привычку по ID и user_id
        habit = await session.get(HabitModel, habit_id)
        if habit and habit.user_id == user_id:  # Проверяем, принадлежит ли привычка пользователю
            await session.delete(habit)  # Удаляем привычку
            await session.commit()  # Сохраняем изменения
            
            
            
async def mark_habit_as_completed(habit_id: int, user_id: int, session: AsyncSession):
    async with session.begin():
        # Находим привычку
        query = await session.execute(select(HabitModel).where(
            HabitModel.Habitid == habit_id, HabitModel.user_id == user_id
        ))
        habit = query.scalars().first()
        
        if habit:
            habit.completed_streak += 1  # Увеличиваем счетчик выполнений
            habit.last_completed_date = datetime.now()  # Устанавливаем дату выполнения
            await session.commit()

async def mark_habit_as_not_completed(habit_id: int, user_id: int, session: AsyncSession):
    async with session.begin():
        # Находим привычку
        query = await session.execute(select(HabitModel).where(
            HabitModel.Habitid == habit_id, HabitModel.user_id == user_id
        ))
        habit = query.scalars().first()
        
        if habit:
            habit.completed_streak = 0  # Сбрасываем счетчик выполнений
            await session.commit()
            


async def get_habit_statistics(habit_id: int):
    async with async_session() as session:
        habit = await session.get(HabitModel, habit_id)
        if habit:
            # Форматирование строки для вывода
            last_completed_date = habit.last_completed_date.strftime('%Y-%m-%d') if habit.last_completed_date else "Не выполнено"
            statistics_message = (
                f"\n"
                f"Название привычки: {habit.Habit_name}\n"
                f"Серия выполнений: {habit.completed_streak}\n"
                f"Последний выполненный день: {last_completed_date}"
            )
            return statistics_message
        
        return "Привычка не найдена."