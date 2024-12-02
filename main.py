import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
import requests

API_TOKEN = '7443024666:AAHUIGFnQ2FyQ_UUSGFTwmimKgV98_C8FYY'
MAIN_ADMIN = [1974800905, 734626776]
API_BASE_URL = "http://localhost:8000/api/messages/messages"
ADMINS_GROUP_ID = -1002442662725
MAIN_ADMINS_GROUP_ID = -4536239336

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type not in ('supergroup', 'group'):
        return

    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if admin.status in ["administrator", "creator"]:
        requests.delete(f"{API_BASE_URL}/{message.chat.id}/delete/")
    else:
        data = {
            "chat_id": message.chat.id,
            "user_id": message.from_user.id,
        }
        response = requests.post(f"{API_BASE_URL}/create/", json=data)
        if response.status_code == 201:
            await asyncio.sleep(180)
            response = requests.get(f"{API_BASE_URL}/{message.chat.id}/")
            if response.status_code == 200:
                record = response.json()
                if record and record['user_id'] == str(message.from_user.id):
                    user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
                    group_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Guruh</a>"
                    try:
                        await bot.send_message(
                            ADMINS_GROUP_ID,
                            f"⚠️ *Ogohlantirish:*\n"
                            f"Foydalanuvchi: {user_link}\n"
                            f"Guruh: {group_link}\n"
                            f"3 daqiqa ichida javob berilmadi.",
                            parse_mode="HTML",
                        )
                    except Exception as e:
                        await bot.send_message(chat_id=MAIN_ADMIN[0], text=str(e))

            await asyncio.sleep(120)
            response = requests.get(f"{API_BASE_URL}/{message.chat.id}/")
            if response.status_code == 200:
                record = response.json()
                if record and record['user_id'] == str(message.from_user.id):
                    requests.delete(f"{API_BASE_URL}/{message.chat.id}/delete/")
                    user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
                    group_link = f"<a href='https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}'>Guruh</a>"
                    try:
                        await bot.send_message(
                            MAIN_ADMINS_GROUP_ID,
                            f"🚨 *Ogohlantirish:*\n"
                            f"Foydalanuvchi: {user_link}\n"
                            f"Guruh: {group_link}\n"
                            f"5 daqiqa ichida javob berilmadi.",
                            parse_mode="HTML",
                        )
                    except Exception as e:
                        await bot.send_message(chat_id=MAIN_ADMIN[0], text=str(e))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
