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


async def send_warning(bot: Bot, user_id: int, chat_id: int, message_id: int, delay: int, warning_type: str):
    await asyncio.sleep(delay)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/{chat_id}/") as response:
            if response.status == 200:
                record = await response.json()
                if record and record['user_id'] == str(user_id):
                    user_link = f"<a href='tg://user?id={user_id}'>{record.get('user_full_name', 'Foydalanuvchi')}</a>"
                    group_info = await bot.get_chat(chat_id)
                    group_name = group_info.title
                    group_link = f"<a href='https://t.me/c/{str(chat_id)[4:]}/{message_id}'>{group_name}</a>"

                    warning_text = (
                        f"⚠️ *Ogohlantirish ({warning_type}):*\n"
                        f"Foydalanuvchi: {user_link}\n"
                        f"Guruh: {group_link}\n"
                        f"{delay // 60} daqiqa ichida javob berilmadi."
                    )
                    try:
                        await bot.send_message(
                            ADMINS_GROUP_ID if warning_type == "3 daqiqa" else MAIN_ADMINS_GROUP_ID,
                            warning_text,
                            parse_mode="HTML",
                        )
                    except Exception as e:
                        await bot.send_message(chat_id=MAIN_ADMIN[0], text=str(e))


async def handle_message(message: types.Message, bot: Bot):
    if message.chat.type not in ('supergroup', 'group'):
        return

    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if admin.status in ["administrator", "creator"]:
        async with aiohttp.ClientSession() as session:
            await session.delete(f"{API_BASE_URL}/{message.chat.id}/delete/")
    else:
        data = {
            "chat_id": message.chat.id,
            "user_id": message.from_user.id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_BASE_URL}/create/", json=data) as response:
                if response.status == 201:
                    asyncio.create_task(
                        send_warning(bot, message.from_user.id, message.chat.id, message.message_id, 180, "3 daqiqa")
                    )
                    asyncio.create_task(
                        send_warning(bot, message.from_user.id, message.chat.id, message.message_id, 300, "5 daqiqa")
                    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
