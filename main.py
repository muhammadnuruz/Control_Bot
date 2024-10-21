import time
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, Boolean, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Logger sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres:1@localhost:5432/control_db"
API_TOKEN = '7443024666:AAHUIGFnQ2FyQ_UUSGFTwmimKgV98_C8FYY'
MAIN_ADMIN = [1974800905, 734626776]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class MessageRecord(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    chat_id = Column(String)
    message_id = Column(String)
    time = Column(Float)
    replied = Column(Boolean, default=False)
    reply_time = Column(Float, nullable=True)


Base.metadata.create_all(engine)

def async_session():
    loop = asyncio.get_event_loop()
    return Session(bind=engine, expire_on_commit=False)

async def record_question(message: types.Message):
    async with async_session() as session:
        try:
            record = MessageRecord(
                user_id=str(message.from_user.id),
                chat_id=str(message.chat.id),
                message_id=str(message.message_id),
                time=time.time()
            )
            session.add(record)
            session.commit()
        except Exception as e:
            logger.error(f"Error recording question: {e}")

async def record_reply(message: types.Message):
    async with async_session() as session:
        try:
            record = session.query(MessageRecord).filter_by(message_id=str(message.reply_to_message.message_id)).first()
            if record:
                record.replied = True
                record.reply_time = time.time()
                session.commit()
        except Exception as e:
            logger.error(f"Error recording reply: {e}")

@dp.message_handler(Command('statistic'))
async def send_statistics(message: types.Message):
    if message.from_user.id in MAIN_ADMIN:
        async with async_session() as session:
            try:
                total_questions = session.query(MessageRecord).count()
                total_unanswered = session.query(MessageRecord).filter(MessageRecord.replied == False).count()

                one_month_ago = time.time() - (30 * 24 * 60 * 60)
                monthly_questions = session.query(MessageRecord).filter(MessageRecord.time >= one_month_ago).count()
                monthly_unanswered = session.query(MessageRecord).filter(
                    MessageRecord.replied == False,
                    MessageRecord.time >= one_month_ago
                ).count()

                one_week_ago = time.time() - (7 * 24 * 60 * 60)
                weekly_questions = session.query(MessageRecord).filter(MessageRecord.time >= one_week_ago).count()
                weekly_unanswered = session.query(MessageRecord).filter(
                    MessageRecord.replied == False,
                    MessageRecord.time >= one_week_ago
                ).count()

                response = (
                    f"Umumiy savollar: {total_questions}\n"
                    f"Javobsiz savollar: {total_unanswered}\n\n"
                    f"Oylik savollar: {monthly_questions}\n"
                    f"Oylik javobsiz savollar: {monthly_unanswered}\n\n"
                    f"Haftalik savollar: {weekly_questions}\n"
                    f"Haftalik javobsiz savollar: {weekly_unanswered}"
                )

                await message.reply(response)
            except Exception as e:
                logger.error(f"Error generating statistics: {e}")

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type not in ['supergroup', 'group']:
        return

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    logger.info(f"Chat member info: {member}")

    if member.status in ["administrator", "creator"]:
        if message.reply_to_message:
            await record_reply(message)
        return

    await record_question(message)

    await asyncio.sleep(180)
    async with async_session() as session:
        record = session.query(MessageRecord).filter_by(message_id=str(message.message_id)).first()

        if record and not record.replied:
            user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            group_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Guruh</a>"
            message_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Xabar</a>"

            try:
                await bot.send_message(
                    -1002442662725,
                    f"Foydalanuvchi: {user_link}\nGuruh: {group_link}\nXabar: {message_link}\n"
                    f"Javob berilmagan: 3 daqiqa ichida javob berilmagan.\nHabar: {message.text}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Error sending message after 3 minutes: {e}")

    await asyncio.sleep(120)
    async with async_session() as session:
        record = session.query(MessageRecord).filter_by(message_id=str(message.message_id)).first()

        if record and not record.replied:
            try:
                await bot.send_message(
                    -4536239336,
                    f"Foydalanuvchi: {user_link}\nGuruh: {group_link}\nXabar: {message_link}\n"
                    f"Javob berilmagan: 5 daqiqa ichida javob berilmagan.\n\nHabar: {message.text}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Error sending message after 5 minutes: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
