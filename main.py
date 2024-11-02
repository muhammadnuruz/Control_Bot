import asyncio
import time
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor

API_TOKEN = '7443024666:AAHUIGFnQ2FyQ_UUSGFTwmimKgV98_C8FYY'
MAIN_ADMIN = [1974800905, 734626776]
API_BASE_URL = "http://localhost:8000/api/messages/messages"  # Django server URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def record_question(message: types.Message):
    data = {
        "user_id": str(message.from_user.id),
        "chat_id": str(message.chat.id),
        "message_id": str(message.message_id),
        "replied": False
    }
    response = requests.post(f"{API_BASE_URL}/create/", json=data)
    if response.status_code != 201:
        print(f"ERROR: Failed to record question. Status code: {response.status_code}")


def record_reply(message: types.Message):
    reply_message_id = message.reply_to_message.message_id
    data = {"replied": True}
    response = requests.patch(f"{API_BASE_URL}/{reply_message_id}/update/", json=data)
    if response.status_code != 200:
        print(f"ERROR: Failed to record reply. Status code: {response.status_code}")


@dp.message_handler(Command('statistic'))
async def send_statistics(message: types.Message):
    if message.from_user.id in MAIN_ADMIN:
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            stats = response.json()
            response_text = (
                f"Umumiy savollar: {stats['total_questions']}\n"
                f"Javob berilmagan savollar: {stats['total_unanswered']}\n\n"
                f"Oylik savollar: {stats['monthly_questions']}\n"
                f"Oylik javob berilmagan savollar: {stats['monthly_unanswered']}\n\n"
                f"Heftalik savollar: {stats['weekly_questions']}\n"
                f"Haftalik javob berilmagan savollar: {stats['weekly_unanswered']}"
            )
            await message.reply(response_text)
        else:
            await message.reply("Statistikani olishda xatolik yuz berdi.")


@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type not in ('supergroup', 'group'):
        return

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status in ["administrator", "creator"]:
        if message.reply_to_message:
            record_reply(message)
        return

    record_question(message)

    await asyncio.sleep(180)
    response = requests.get(f"{API_BASE_URL}/{message.message_id}/")
    if response.status_code == 200:
        record = response.json()
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

        response = requests.get(f"{API_BASE_URL}/{message.message_id}/")
        if response.status_code == 200:
            record_2 = response.json()
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
