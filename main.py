DATABASE_URL = "postgresql://postgres:1@localhost:5432/control_db"
API_TOKEN = '7443024666:AAHUIGFnQ2FyQ_UUSGFTwmimKgV98_C8FYY'
MAIN_ADMIN = [1974800905, 734626776]
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, Boolean, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


def record_question(message: types.Message):
    session = Session()
    record = MessageRecord(
        user_id=str(message.from_user.id),
        chat_id=str(message.chat.id),
        message_id=str(message.message_id),
        time=time.time()
    )
    session.add(record)
    session.commit()
    session.close()


def record_reply(message: types.Message):
    session = Session()
    record = session.query(MessageRecord).filter_by(message_id=str(message.reply_to_message.message_id)).first()
    if record:
        record.replied = True
        record.reply_time = time.time()
        session.commit()
    session.close()


@dp.message_handler(Command('statistic'))
async def send_statistics(message: types.Message):
    if message.from_user.id in MAIN_ADMIN:
        session = Session()
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
            f"Umumiy savollar: {total_questions}\n 5 daqiqa ichida javob berilmagan savollar: {total_unanswered}\n\n"
            f"Oylik savollar: {monthly_questions}\n oylik javob berilmagan savollar: {monthly_unanswered}\n\n"
            f"Heftalik savollar: {weekly_questions}\n haftalik javob berilmagan savollar: {weekly_unanswered}")

        await message.reply(response)
        session.close()


@dp.message_handler()
async def handle_message(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if message.reply_to_message:
        if member.status in ["administrator", "creator"]:
            record_reply(message)
        return

    if message.chat.type != 'supergroup' and message.chat.type != 'group' or member.status in ["administrator",
                                                                                               "creator"]:
        return

    record_question(message)

    await asyncio.sleep(300)
    session = Session()
    record = session.query(MessageRecord).filter_by(message_id=str(message.message_id)).first()

    if record and not record.replied:
        user_link = f"[{message.from_user.full_name}](tg://user?id={message.from_user.id} )"
        group_link = f"[Guruh](https://t.me/c/{message.chat.id}/{message.message_id})"
        message_link = f"[Xabar](https://t.me/c/{message.chat.id}/{message.message_id})"
        for admin in MAIN_ADMIN:
            try:
                await bot.send_message(admin,
                                       f"Foydalanuvchi: {user_link}\n"
                                       f"Guruh: {group_link}\n"
                                       f"Xabar: {message_link}\n"
                                       f"Javob berilmagan: 5 daqiqa ichida javob berilmagan.")
            except Exception:
                pass

    session.close()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
