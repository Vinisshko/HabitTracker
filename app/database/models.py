import os
from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#import os, sqlite3 #удалила старую бд
from dotenv import load_dotenv



load_dotenv()
database_url = os.getenv('DATABASE_URL')

# Создание асинхронного двигателя
engine = create_async_engine(url=database_url)

async def async_main():
       async with engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    habits = relationship("HabitModel", back_populates="user")   
    
class HabitModel(Base): 
    __tablename__ = 'habit'  # Исправлено на __tablename__ 
     
    #id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Автоинкремент идентификатор
    Habitid = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Автоинкремент идентификатор
    Habit_name = Column(String(25), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    completed_streak = Column(Integer, default=0) 
    last_completed_date = Column(DateTime)
    
    user = relationship("User", back_populates="habits")
    