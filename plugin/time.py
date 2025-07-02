from datetime import datetime, timezone, timedelta
from pyrogram import Client
from pyrogram.types import Message

command = "time"

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        timezone_str = settings.get("time_timezone", "UTC+3")
        
        # Проверка формата часового пояса
        if not timezone_str.startswith("UTC") or len(timezone_str) < 4:
            await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Неверный формат часового пояса!
├─▶ ⚠️ Используйте настройку .nast time
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        offset_str = timezone_str[3:]
        try:
            offset_hours = float(offset_str)
        except ValueError:
            await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Ошибка в значении смещения!
├─▶ ⚠️ Используйте настройку .nast time
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return
            
        offset = timedelta(hours=offset_hours)
        custom_timezone = timezone(offset)

        current_time = datetime.now(custom_timezone)
        day_of_week = current_time.strftime("%A")
        date = current_time.strftime("%d.%m.%Y")
        time_str = current_time.strftime("%H:%M:%S")

        result = f"""
╭────⋞⏳ TIME INFO ⏳⋟───╮
│
├─▶ 📅 День недели: {day_of_week}
├─▶ 🗓 Дата: {date}
├─▶ 🕒 Время: {time_str}
├─▶ 🌏 Временная зона: {timezone_str}
│
╰───⋞🌌 Powered by Cosmo 🌌⋟
"""
        await message.reply(result)
    except Exception as e:
        await message.reply(f"""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Произошла ошибка!
├─▶ ⚠️ Error: {e}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
