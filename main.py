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

# Отключение логирования в консоль если нужно
if not settings.get("console_logging", True):
    logging.getLogger().handlers = []
    logger.info("Console logging disabled")

# Создаём папки для плагинов
os.makedirs("plugin", exist_ok=True)
os.makedirs("plugin_sist", exist_ok=True)

app = Client(
    "my_user_bot",
    api_id=21004939,
    api_hash="05b2b4afbae9aecfd3dfd34893afff6f",
    workers=4,
    sleep_threshold=60,
    max_concurrent_transmissions=100,
    retry_delay=3,
    timeout=300
)

def load_commands():
    commands = {}
    # Загрузка из plugin
    for filename in os.listdir("plugin"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                module_name = filename[:-3]
                module = __import__(f"plugin.{module_name}", fromlist=[module_name])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
                    logger.info(f"Command '{module.command}' loaded from plugin/{filename}")
            except Exception as e:
                logger.error(f"Failed to load command plugin/{filename}: {e}")
    
    # Загрузка из plugin_sist
    for filename in os.listdir("plugin_sist"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                module_name = filename[:-3]
                module = __import__(f"plugin_sist.{module_name}", fromlist=[module_name])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
                    logger.info(f"System command '{module.command}' loaded from plugin_sist/{filename}")
            except Exception as e:
                logger.error(f"Failed to load system command plugin_sist/{filename}: {e}")
    return commands

commands = load_commands()

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

        if command in commands:
            logger.info(f"Executing: {command}")
            start_time = time.time()
            try:
                await commands[command](client, message, args, settings)
                logger.info(f"Command '{command}' executed in {time.time() - start_time:.2f}s")
            except Exception as e:
                logger.error(f"Error in {command}: {e}")
                await message.reply(f"""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Ошибка выполнения!
├─▶ 🐞 {str(e)}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        else:
            logger.warning(f"Unknown command: {command}")
            await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Неизвестная команда!
├─▶ 🔍 {command}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")

    except (PeerIdInvalid, ChannelInvalid) as e:
        logger.warning(f"Invalid peer/channel: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    logger.info("Starting bot...")
    app.run()