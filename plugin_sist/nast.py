from pyrogram import Client
from pyrogram.types import Message
from main import save_settings

command = "nast"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not args:
        await message.reply("""
╭───⋞⚙️ SYSTEM SETTINGS ⚙️⋟───╮
├─▶ ⚙️ Доступные настройки:
│
├─ ▶️ Время:
├─ .nast time <UTC±X>
├─ Пример: .nast time UTC+5
│
├─ ▶️ Логирование:
├─ .nast log <on/off>
├─ on - вывод логов в консоль
├─ off - скрыть логи в консоли
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Неверный формат команды!
├─▶ 💡 Используйте: .nast <настройка> <значение>
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    action, value = parts[0].lower(), parts[1]

    if action == "time":
        if not value.startswith("UTC") or len(value) < 4:
            await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Неверный формат часового пояса!
├─▶ 💡 Пример: UTC+3, UTC-5
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        try:
            offset = float(value[3:])
            if not -12 <= offset <= 14:
                await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Недопустимое смещение!
├─▶ 🔢 Допустимый диапазон: -12 до +14
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                return

            settings["time_timezone"] = value
            save_settings(settings)
            await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ✅ Часовой пояс установлен:
├─▶ ⏰ {value}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        except ValueError:
            await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Ошибка значения смещения!
├─▶ 🔢 Используйте число (например: 3 или -4)
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
    
    elif action == "log":
        if value.lower() in ["on", "off"]:
            settings["console_logging"] = (value.lower() == "on")
            save_settings(settings)
            status = "ВКЛЮЧЕНО" if value.lower() == "on" else "ВЫКЛЮЧЕНО"
            await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ✅ Логирование в консоль:
├─▶ 📋 {status}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        else:
            await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Неверное значение!
├─▶ 💡 Используйте: on или off
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
    
    else:
        await message.reply(f"""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Неизвестная настройка!
├─▶ 🔍 {action}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
