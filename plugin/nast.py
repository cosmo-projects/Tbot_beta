from pyrogram import Client
from pyrogram.types import Message
from main import save_settings
from config_sist import COMMAND_PREFIXES

command = "nast"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not args:
        await message.reply("""
╭───⋞⚙️ SYSTEM SETTINGS ⚙️⋟───╮
├─▶ ⚙️ Available settings:
├─▶ .nast time <UTC±X> - timezone
├─▶ .nast aliaspref <on/off> - alias prefixes
├─▶ on - requires prefix (.l/azi/.tlp)
├─▶ off - aliases without prefix
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Invalid command format
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    action, value = parts[0].lower(), parts[1].lower()

    if action == "time":
        if not value.startswith("UTC") or len(value) < 4:
            await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Invalid timezone format
├─▶ Example: UTC+3, UTC-5
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        try:
            offset = float(value[3:])
            if not -12 <= offset <= 14:
                await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Offset must be between -12 and +14
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                return

            settings["time_timezone"] = value
            save_settings(settings)
            await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ✅ Timezone set to: {value}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        except ValueError:
            await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Invalid offset format
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        
    elif action == "aliaspref":
        if value in ["on", "off"]:
            settings["alias_settings"]["require_prefix"] = (value == "on")
            save_settings(settings)
            status = "ENABLED" if value == "on" else "DISABLED"
            await message.reply(f"""
╭───⋞⚙️ ALIAS PREFIXES ⚙️⋟───╮
├─▶ ✅ Alias prefixes: {status}
├─▶ {'Requires prefix: ' + ', '.join(COMMAND_PREFIXES) if value == 'on' else 'Aliases work without prefix'}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        else:
            await message.reply("""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
├─▶ ❗ Invalid value
├─▶ Use: on or off
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
    else:
        await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Unknown setting
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
