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
COMMAND_PREFIXES = [".l", "azi", ".tlp"]

# Файл для хранения настроек
SETTINGS_FILE = "conf.json"

def load_settings():
    default_settings = {"time_timezone": "UTC+3"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                loaded_settings = json.load(f)
                for key, value in default_settings.items():
                    if key not in loaded_settings:
                        loaded_settings[key] = value
                return loaded_settings
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

app = Client(
    "my_user_bot",
    api_id=ВСТАВТЕ ЗНАЧЕНИЕ,
    api_hash="ВСИАВТЕ ЗНАЧЕНИЕ"
)

def load_commands():
    commands = {}
    if not os.path.exists("bot_cmd"):
        logger.warning("Directory 'bot_cmd' not found")
        return commands
    
    for filename in os.listdir("bot_cmd"):
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

@app.on_message(filters.private | filters.group)
async def handle_commands(client: Client, message: Message):
    try:
        text = message.text or message.caption
        if not text or not text.startswith(tuple(COMMAND_PREFIXES)):
            return

        prefix = next(p for p in COMMAND_PREFIXES if text.startswith(p))
        command_part = text[len(prefix):].strip()
        if not command_part:
            return

        command = command_part.split()[0].lower()
        args = command_part[len(command):].strip()

        if command in commands:
            logger.info(f"Executing: {command}")
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
    logger.info("Starting bot...")
    app.run()
