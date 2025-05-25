import os
import time
import logging
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from config_sist import COMMAND_PREFIXES, DEFAULT_SETTINGS

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Файл для хранения настроек
SETTINGS_FILE = "conf.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                loaded_settings = json.load(f)
                return {**DEFAULT_SETTINGS, **loaded_settings}
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")

settings = load_settings()

# Создаём папку для плагинов
os.makedirs("plugin", exist_ok=True)

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
                module = __import__(f"plugin.{module_name}", fromlist=[module_name])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
                    logger.info(f"Command '{module.command}' loaded from {filename}")
            except Exception as e:
                logger.error(f"Failed to load command {filename}: {e}")
    return commands

commands = load_commands()

def resolve_alias(command: str, args: str, settings: dict) -> tuple:
    """Разрешает алиасы команд с учетом префиксов"""
    aliases = settings.get("aliases", {})
    alias_settings = settings.get("alias_settings", {})
    require_prefix = alias_settings.get("require_prefix", True)
    
    full_command = f"{command} {args}".strip()
    
    if require_prefix:
        for prefix in COMMAND_PREFIXES:
            prefixed_cmd = f"{prefix}{full_command}"
            if prefixed_cmd in aliases:
                new_cmd = aliases[prefixed_cmd]
                return new_cmd.split(maxsplit=1) if " " in new_cmd else (new_cmd, "")
    
    if not require_prefix:
        if full_command in aliases:
            new_cmd = aliases[full_command]
            return new_cmd.split(maxsplit=1) if " " in new_cmd else (new_cmd, "")
        
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

        prefix = next((p for p in COMMAND_PREFIXES if text.startswith(p)), None)
        if not prefix:
            return

        command_part = text[len(prefix):].strip()
        if not command_part:
            return

        command = command_part.split()[0].lower()
        args = command_part[len(command):].strip()

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
    logger.info("Starting bot...")
    app.run()
