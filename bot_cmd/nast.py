from pyrogram import Client
from pyrogram.types import Message
from main import save_settings
import os

command = "nast"

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        if not args:
            await message.reply("⚠️ Usage: .nast times UTC+3")
            return

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            await message.reply("⚠️ Example: .nast times UTC+3")
            return

        target_command, setting_value = parts

        if target_command.lower() == "times":
            if not setting_value.startswith("UTC") or len(setting_value) < 4:
                await message.reply("⚠️ Format: UTC±X (e.g., UTC+3, UTC-5)")
                return

            try:
                offset_str = setting_value[3:]
                offset_hours = float(offset_str)
                if not -12 <= offset_hours <= 14:
                    await message.reply("⚠️ Offset must be between -12 and +14")
                    return

                settings["time_timezone"] = setting_value
                save_settings(settings)
                await message.reply(f"✅ Timezone set to {setting_value}")
            except ValueError:
                await message.reply("⚠️ Invalid format. Use UTC±X")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")
