from pyrogram import Client
from pyrogram.types import Message
from main import save_settings

command = "nast"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not args:
        await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ⚠️ Использование: .nast times UTC+3
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Неверный формат команды
├─▶ ✅ Пример: .nast times UTC+3
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    target_command, setting_value = parts

    if target_command.lower() == "times":
        if not setting_value.startswith("UTC") or len(setting_value) < 4:
            await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Неверный формат временной зоны
├─▶ ⚠️ Формат: UTC±X (например, UTC+3, UTC-5)
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        try:
            offset_str = setting_value[3:]
            offset_hours = float(offset_str)
            if not -12 <= offset_hours <= 14:
                await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Недопустимое значение
├─▶ ⚠️ Смещение должно быть между -12 и +14
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                return

            settings["time_timezone"] = setting_value
            save_settings(settings)
            await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ✅ Временная зона успешно установлена
├─▶ 🕒 Текущая зона: {setting_value}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        except ValueError:
            await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Неверный формат смещения
├─▶ ⚠️ Используйте UTC±X (например, UTC+3)
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
