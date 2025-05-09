from datetime import datetime, timezone, timedelta
from pyrogram import Client
from pyrogram.types import Message

command = "time"

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        timezone_str = settings.get("time_timezone", "UTC+3")
        offset_str = timezone_str[3:]
        offset_hours = float(offset_str)
        offset = timedelta(hours=offset_hours)
        custom_timezone = timezone(offset)

        current_time = datetime.now(custom_timezone)
        day_of_week = current_time.strftime("%A")
        date = current_time.strftime("%d.%m.%Y")
        time_str = current_time.strftime("%H:%M:%S")

        result = f"""
⏳═════⋆⋅> TIME INFO  
│ 
├─▶ Day: {day_of_week} 
├─▶ Date: {date} 
├─▶ Time: {time_str} 
├─▶ Timezone: {timezone_str} 
│ 
╰═════⋆⋅> Powered by Cosmo
        """
        await message.reply(result)
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")
