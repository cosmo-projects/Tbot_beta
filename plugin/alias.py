 from pyrogram import Client
from pyrogram.types import Message
from main import save_settings
from config_sist import COMMAND_PREFIXES

command = "alias"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not args:
        aliases = settings.get("aliases", {})
        require_prefix = settings["alias_settings"].get("require_prefix", True)
        
        if not aliases:
            await message.reply("""
╭───⋞⚙️ ALIAS INFO ⚙️⋟───╮
├─▶ ℹ️ No aliases configured
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        response = "╭───⋞⚙️ ALIAS LIST ⚙️⋟───╮\n│\n"
        for alias, target in aliases.items():
            response += f"├─▶ {alias} → {target}\n"
        
        response += f"│\n├─▶ {'🟢' if require_prefix else '🔴'} Prefixes: {'Required' if require_prefix else 'Not required'}\n"
        response += "╰───⋞🌌 Powered by Cosmo 🌌⋟"
        
        await message.reply(response)
        return

    parts = args.split(maxsplit=2)
    if len(parts) < 2:
        await message.reply("""
╭───⋞⚙️ ALIAS USAGE ⚙️⋟───╮
├─▶ Usage:
├─▶ .alias add <alias> <command>
├─▶ .alias del <alias>
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        return

    action, alias = parts[0].lower(), parts[1]
    require_prefix = settings["alias_settings"].get("require_prefix", True)

    if action == "add":
        if len(parts) < 3:
            await message.reply("""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
├─▶ ❗ Specify target command
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        target = parts[2]
        
        if require_prefix and not any(alias.startswith(p) for p in COMMAND_PREFIXES):
            await message.reply(f"""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
├─▶ ❗ Alias must start with:
├─▶ {', '.join(COMMAND_PREFIXES)}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return

        settings["aliases"][alias] = target
        save_settings(settings)
        await message.reply(f"""
╭───⋞⚙️ ALIAS ADDED ⚙️⋟───╮
├─▶ ✅ Alias added:
├─▶ {alias} → {target}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")

    elif action == "del":
        if alias in settings["aliases"]:
            del settings["aliases"][alias]
            save_settings(settings)
            await message.reply(f"""
╭───⋞⚙️ ALIAS REMOVED ⚙️⋟───╮
├─▶ ✅ Alias removed: {alias}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        else:
            await message.reply(f"""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
├─▶ ❗ Alias not found: {alias}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
    else:
        await message.reply(f"""
╭───⋞⚙️ ALIAS ERROR ⚙️⋟───╮
├─▶ ❗ Unknown action: {action}
├─▶ Use add/del
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
