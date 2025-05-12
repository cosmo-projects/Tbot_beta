import time
import platform
from datetime import datetime
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import __version__ as pyrogram_version

command = "ping"

async def handler(client: Client, message: Message, args: str, settings: dict):
    start_time = time.time()
    api_ping = await get_telegram_api_ping(client)
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    result = f"""
╭───⋞⚙️ SYSTEM STATUS ⚙️⋟───╮
│
├─▶ 🚀 PING: {(time.time() - start_time)*1000:.2f} ms
├─▶ 📡 API: {api_ping:.2f} ms
├─▶ 🕒 Time: {current_time}
│
├─◈ 🐍 Python: {platform.python_version()}
├─◈ 🔥 Pyrogram: {pyrogram_version}
├─◈ 💻 System: {platform.system()} {platform.release()}
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
"""
    await message.reply(result)

async def get_telegram_api_ping(client: Client):
    start = time.time()
    await client.get_me()
    return (time.time() - start) * 1000
