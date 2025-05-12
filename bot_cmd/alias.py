from pyrogram import Client
from pyrogram.types import Message
from main import save_settings

command = "alias"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not args:
        # Показать все алиасы
        aliases = settings.get("aliases", {})
        if not aliases:
            await message.reply("""
╭───⋞⚙️ ALIAS INFO ⚙️⋟───╮
│
├─▶ ℹ️ Алиасы не настроены
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
            return

        response = "╭───⋞⚙️ ALIAS LIST ⚙️⋟───╮\n│\n"
        for alias, target in aliases.items():
            response += f"├─▶ {alias} → {target}\n"
        response += "│\n╰───⋞🌌 Powered by Cosmo 🌌⋟───╯"
        
        await message.reply(response)
        return

    parts = args.split(maxsplit=2)
    if len(parts) < 2:
        await message.reply("""
╭───⋞⚙️ ALIAS USAGE ⚙️⋟───╮
│
├─▶ ⚠️ Использование:
├─▶ .alias add <алиас> <команда>
├─▶ .alias del <алиас>
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
        return

    action = parts[0].lower()
    alias = parts[1].lower()

    if action == "add":
        if len(parts) < 3:
            await message.reply("""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
│
├─▶ ❗ Укажите команду для алиаса
├─▶ ✅ Пример: .alias add d del
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
            return

        target = parts[2]
        settings["aliases"][alias] = target
        save_settings(settings)
        await message.reply(f"""
╭───⋞⚙️ ALIAS ADDED ⚙️⋟───╮
│
├─▶ ✅ Алиас добавлен:
├─▶ {alias} → {target}
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")

    elif action == "del":
        if alias in settings["aliases"]:
            del settings["aliases"][alias]
            save_settings(settings)
            await message.reply(f"""
╭───⋞⚙️ ALIAS REMOVED ⚙️⋟───╮
│
├─▶ ✅ Алиас удалён: {alias}
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
        else:
            await message.reply(f"""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
│
├─▶ ❗ Алиас не найден: {alias}
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
    else:
        await message.reply(f"""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
│
├─▶ ❗ Неизвестное действие: {action}
├─▶ Используйте add/del
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
