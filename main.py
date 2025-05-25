import os
import time
import logging
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Префиксы команд
COMMAND_PREFIXES = [".l", "azi", ".tlp", "!"]

# Файл для хранения настроек
SETTINGS_FILE = "conf.json"

# Алиасы команд
COMMAND_ALIASES = {
    "fix": "pin"
}

def load_settings():
    default_settings = {
        "time_timezone": "UTC+3",
        "aliases": COMMAND_ALIASES
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                loaded_settings = json.load(f)
                # Объединяем с настройками по умолчанию
                return {**default_settings, **loaded_settings}
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return default_settings
    return default_settings

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")

settings = load_settings()

# Создаём папку для модулей, если её нет
os.makedirs("bot_cmd", exist_ok=True)

app = Client(
    "my_user_bot",
    api_id=21004939,
    api_hash="05b2b4afbae9aecfd3dfd34893afff6f"
)

def load_commands():
    commands = {}
    for filename in os.listdir("plugin"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                module_name = filename[:-3]
                module = __import__(f"bot_cmd.{module_name}", fromlist=[module_name])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
                    logger.info(f"Command '{module.command}' loaded")
            except Exception as e:
                logger.error(f"Failed to load command {filename}: {e}")
    return commands

commands = load_commands()

def resolve_alias(command: str, args: str, settings: dict) -> tuple:
    """Разрешает алиасы команд"""
    aliases = settings.get("aliases", {})
    
    # Проверяем полную команду с аргументами
    full_command = f"{command} {args}".strip()
    if full_command in aliases:
        new_cmd = aliases[full_command]
        return new_cmd.split(maxsplit=1) if " " in new_cmd else (new_cmd, "")
    
    # Проверяем только команду
    if command in aliases:
        new_cmd = aliases[command]
        return new_cmd.split(maxsplit=1) + [args] if " " in new_cmd else (new_cmd, args)
    
    return command, args

@app.on_message(filters.private | filters.group)
async def handle_commands(client: Client, message: Message):
    try:
        text = message.text or message.caption
        if not text:
            return

        # Проверяем все префиксы
        prefix = next((p for p in COMMAND_PREFIXES if text.startswith(p)), None)
        if not prefix:
            return

        command_part = text[len(prefix):].strip()
        if not command_part:
            return

        command = command_part.split()[0].lower()
        args = command_part[len(command):].strip()

        # Обрабатываем алиасы
        command, args = resolve_alias(command, args, settings)

        if command in commands:
            logger.info(f"Executing: {command} (original: {text})")
            start_time = time.time()
            try:
                await commands[command](client, message, args, settings)
                logger.info(f"Command '{command}' executed in {time.time() - start_time:.2f}s")
            except Exception as e:
                logger.error(f"Error in {command}: {e}")
                await message.reply(f"⚠️ Error: {e}")
        else:
            logger.warning(f"Unknown command: {command}")
            await message.reply("❌ Unknown command")

    except (PeerIdInvalid, ChannelInvalid) as e:
        logger.warning(f"Invalid peer/channel: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    logger.info("Starting bot in Termux...")
    app.run()
