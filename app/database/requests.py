from app.database.models import async_session
from app.database.models import User, HabitModel
from sqlalchemy import select


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
       
       
async def save_habit(new_habit):        
    async with async_session() as session: 
        habit = HabitModel(Habit_name=new_habit)  # Создаем новый объект Habit 
        session.add(habit)  # Добавляем его в сессию 
        await session.commit()  # Сохраняем изменения в базе данных

        