import time
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor

API_TOKEN = '7443024666:AAHUIGFnQ2FyQ_UUSGFTwmimKgV98_C8FYY'
MAIN_ADMIN = [1974800905, 734626776]
API_BASE_URL = "http://localhost:8000/api/messages"  # Change this to your Django server URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def record_question(message: types.Message):
    async with aiohttp.ClientSession() as session:
        data = {
            "user_id": str(message.from_user.id),
            "chat_id": str(message.chat.id),
            "message_id": str(message.message_id),
            "time": time.time()
        }
        await session.post(f"{API_BASE_URL}/", json=data)


async def record_reply(message: types.Message):
    async with aiohttp.ClientSession() as session:
        reply_message_id = message.reply_to_message.message_id
        data = {"replied": True, "reply_time": time.time()}
        await session.patch(f"{API_BASE_URL}/{reply_message_id}/", json=data)


@dp.message_handler(Command('statistic'))
async def send_statistics(message: types.Message):
    if message.from_user.id in MAIN_ADMIN:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}/statistics/") as response:
                stats = await response.json()
                response_text = (
                    f"Umumiy savollar: {stats['total_questions']}\n"
                    f"Javob berilmagan savollar: {stats['total_unanswered']}\n\n"
                    f"Oylik savollar: {stats['monthly_questions']}\n"
                    f"Oylik javob berilmagan savollar: {stats['monthly_unanswered']}\n\n"
                    f"Heftalik savollar: {stats['weekly_questions']}\n"
                    f"Haftalik javob berilmagan savollar: {stats['weekly_unanswered']}"
                )
                await message.reply(response_text)


@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type not in ('supergroup', 'group'):
        return

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status in ["administrator", "creator"]:
        if message.reply_to_message:
            await record_reply(message)
        return

    await record_question(message)

    await asyncio.sleep(180)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/{message.message_id}/") as response:
            record = await response.json()

        if record.get("replied"):
            return

        user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
        group_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Guruh</a>"
        message_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Xabar</a>"

        try:
            await bot.send_message(-1002442662725,
                                   f"Foydalanuvchi: {user_link}\nGuruh: {group_link}\nXabar: {message_link}\n"
                                   f"Javob berilmagan: 3 daqiqa ichida javob berilmagan.\nHabar: {message.text}",
                                   parse_mode="HTML")
        except Exception as e:
            await bot.send_message(chat_id=1974800905, text=str(e))

        await asyncio.sleep(120)

        async with session.get(f"{API_BASE_URL}/{message.message_id}/") as response:
            record_2 = await response.json()

        if record_2.get("replied"):
            return
        else:
            try:
                await bot.send_message(-4536239336,
                                       f"Foydalanuvchi: {user_link}\n"
                                       f"Guruh: {group_link}\n"
                                       f"Xabar: {message_link}\n"
                                       f"Javob berilmagan: 5 daqiqa ichida javob berilmagan.\n\n"
                                       f"Habar: {message.text}",
                                       parse_mode="HTML")
            except Exception as e:
                await bot.send_message(chat_id=1974800905, text=str(e))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
