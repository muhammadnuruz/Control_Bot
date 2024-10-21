import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, Boolean, Float, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost:5432/control_db"
API_TOKEN = '7443024666:AAHUIGFnQ2FyQ_UUSGFTwmimKgV98_C8FYY'
MAIN_ADMIN = [1974800905, 734626776]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Create the async engine and session
async_engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class MessageRecord(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    chat_id = Column(String)
    message_id = Column(String)
    time = Column(Float)
    replied = Column(Boolean, default=False)
    reply_time = Column(Float, nullable=True)


# Create all tables
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def record_question(message: types.Message):
    async with AsyncSessionLocal() as session:
        record = MessageRecord(
            user_id=str(message.from_user.id),
            chat_id=str(message.chat.id),
            message_id=str(message.message_id),
            time=time.time()
        )
        session.add(record)
        await session.commit()


async def record_reply(message: types.Message):
    async with AsyncSessionLocal() as session:
        record = await session.execute(
            session.query(MessageRecord).filter_by(message_id=str(message.reply_to_message.message_id))
        )
        record = record.scalar_one_or_none()
        if record:
            record.replied = True
            record.reply_time = time.time()
            await session.commit()


@dp.message_handler(Command('statistic'))
async def send_statistics(message: types.Message):
    if message.from_user.id in MAIN_ADMIN:
        async with AsyncSessionLocal() as session:
            total_questions = (await session.execute(
                session.query(MessageRecord).count()
            )).scalar()

            total_unanswered = (await session.execute(
                session.query(MessageRecord).filter(MessageRecord.replied == False).count()
            )).scalar()

            one_month_ago = time.time() - (30 * 24 * 60 * 60)
            monthly_questions = (await session.execute(
                session.query(MessageRecord).filter(MessageRecord.time >= one_month_ago).count()
            )).scalar()

            monthly_unanswered = (await session.execute(
                session.query(MessageRecord).filter(MessageRecord.replied == False,
                                                     MessageRecord.time >= one_month_ago).count()
            )).scalar()

            one_week_ago = time.time() - (7 * 24 * 60 * 60)
            weekly_questions = (await session.execute(
                session.query(MessageRecord).filter(MessageRecord.time >= one_week_ago).count()
            )).scalar()

            weekly_unanswered = (await session.execute(
                session.query(MessageRecord).filter(MessageRecord.replied == False,
                                                     MessageRecord.time >= one_week_ago).count()
            )).scalar()

            response = (
                f"Umumiy savollar: {total_questions}\n"
                f"5 daqiqa ichida javob berilmagan savollar: {total_unanswered}\n\n"
                f"Oylik savollar: {monthly_questions}\n"
                f"Oylik javob berilmagan savollar: {monthly_unanswered}\n\n"
                f"Heftalik savollar: {weekly_questions}\n"
                f"Haftalik javob berilmagan savollar: {weekly_unanswered}"
            )

            await message.reply(response)


@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type not in ['supergroup', 'group']:
        return

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    await bot.send_message(chat_id=1974800905, text=f"{member}")
    if member.status in ["administrator", "creator"]:
        if message.reply_to_message:
            await record_reply(message)
        return

    await record_question(message)

    await asyncio.sleep(180)

    async with AsyncSessionLocal() as session:
        record = (await session.execute(
            session.query(MessageRecord).filter_by(message_id=str(message.message_id))
        )).scalar_one_or_none()

        if record and not record.replied:
            user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            group_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Guruh</a>"
            message_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Xabar</a>"

            try:
                await bot.send_message(-1002442662725,
                                       f"Foydalanuvchi: {user_link}\n"
                                       f"Guruh: {group_link}\n"
                                       f"Xabar: {message_link}\n"
                                       f"Javob berilmagan: 3 daqiqa ichida javob berilmagan.\n"
                                       f"Habar: {message.text}",
                                       parse_mode="HTML")
            except Exception as e:
                await bot.send_message(chat_id=1974800905, text=f"{e}")

    await asyncio.sleep(120)

    async with AsyncSessionLocal() as session:
        record = (await session.execute(
            session.query(MessageRecord).filter_by(message_id=str(message.message_id))
        )).scalar_one_or_none()

        if record and not record.replied:
            try:
                await bot.send_message(-4536239336,
                                       f"Foydalanuvchi: {user_link}\n"
                                       f"Guruh: {group_link}\n"
                                       f"Xabar: {message_link}\n"
                                       f"Javob berilmagan: 5 daqiqa ichida javob berilmagan.\n\n"
                                       f"Habar: {message.text}",
                                       parse_mode="HTML")
            except Exception as e:
                await bot.send_message(chat_id=1974800905, text=f"{e}")


if __name__ == "__main__":
    asyncio.run(init_db())  # Initialize the database
    executor.start_polling(dp, skip_updates=True)
