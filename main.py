import os
import sys
import time
import json
import logging
import argparse
from colorama import init, Fore, Style
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from config_sist import COMMAND_PREFIXES, DEFAULT_SETTINGS

# Проверка и установка TgCrypto
try:
    import TgCrypto
except ImportError:
    print(f"\n{Fore.YELLOW}⚠️ TgCrypto не установлен! Производительность будет ниже.")
    print(f"{Fore.CYAN}Установите его командой: {Style.BRIGHT}{Fore.GREEN}pip install TgCrypto{Style.RESET_ALL}\n")

# Инициализация colorama
init(autoreset=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format=f'{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - {Fore.BLUE}%(name)s{Style.RESET_ALL} - {Fore.YELLOW}%(levelname)s{Style.RESET_ALL} - %(message)s'
)
logger = logging.getLogger(__name__)

# Файлы конфигурации
SETTINGS_FILE = "conf.json"
API_CONFIG_FILE = "api_config.json"

def print_banner():
    """Печать красивого баннера при запуске"""
    banner = f"""
{Fore.MAGENTA}╔════════════════════════════════════════════════════════════╗
{Fore.MAGENTA}║{Style.BRIGHT}{Fore.CYAN}     ██████╗ ██████╗ ███████╗███╗   ███╗ ██████╗     ██╗   ██╗██████╗ {Fore.MAGENTA}║
{Fore.MAGENTA}║{Fore.CYAN}    ██╔════╝██╔═══██╗██╔════╝████╗ ████║██╔═══██╗    ██║   ██║██╔══██╗{Fore.MAGENTA}║
{Fore.MAGENTA}║{Fore.CYAN}    ██║     ██║   ██║███████╗██╔████╔██║██║   ██║    ██║   ██║██████╔╝{Fore.MAGENTA}║
{Fore.MAGENTA}║{Fore.CYAN}    ██║     ██║   ██║╚════██║██║╚██╔╝██║██║   ██║    ██║   ██║██╔══██╗{Fore.MAGENTA}║
{Fore.MAGENTA}║{Fore.CYAN}    ╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝    ╚██████╔╝██║  ██║{Fore.MAGENTA}║
{Fore.MAGENTA}║{Fore.CYAN}     ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═╝{Fore.MAGENTA}║
{Fore.MAGENTA}║{Style.BRIGHT}{Fore.YELLOW}              TERMINAL USERBOT v2.0 - COSMO EDITION            {Fore.MAGENTA}║
{Fore.MAGENTA}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_header(title):
    """Печать цветного заголовка"""
    header = f"""
{Fore.YELLOW}╔{'═'*60}╗
{Fore.YELLOW}║{Style.BRIGHT}{Fore.CYAN}{title.center(60)}{Fore.YELLOW}║
{Fore.YELLOW}╚{'═'*60}╝{Style.RESET_ALL}
"""
    print(header)

def get_api_credentials():
    """Получение API-данных от пользователя с цветным оформлением"""
    print_header("НАСТРОЙКА ТЕЛЕГРАМ АККАУНТА (API DATA)")
    
    print(f"{Fore.GREEN}ℹ️ Инструкция по получению API ID и API HASH:")
    print(f"{Fore.CYAN}1. Перейдите на {Style.BRIGHT}{Fore.BLUE}https://my.telegram.org")
    print(f"{Fore.CYAN}2. Войдите в свой аккаунт Telegram")
    print(f"{Fore.CYAN}3. Перейдите в раздел 'API development tools'")
    print(f"{Fore.CYAN}4. Создайте новое приложение и скопируйте данные{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}╔{'═'*60}╗")
    print(f"{Fore.MAGENTA}║{Style.BRIGHT}{Fore.CYAN} ВАЖНО: Никому не передавайте эти данные! Они как пароль! {Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}╚{'═'*60}╝{Style.RESET_ALL}\n")
    
    while True:
        try:
            # Ввод API ID с цветной подсказкой
            api_id = input(f"{Style.BRIGHT}{Fore.MAGENTA}↳ Введите ваш {Fore.CYAN}API ID{Fore.MAGENTA} (только цифры): {Style.RESET_ALL}{Fore.YELLOW}")
            if not api_id.isdigit():
                raise ValueError(f"{Fore.RED}API ID должен состоять только из цифр!")
                
            # Ввод API HASH с цветной подсказкой
            api_hash = input(f"{Style.BRIGHT}{Fore.MAGENTA}↳ Введите ваш {Fore.CYAN}API HASH{Fore.MAGENTA} (32 символа): {Style.RESET_ALL}{Fore.YELLOW}")
            if len(api_hash) != 32 or not all(c in "0123456789abcdef" for c in api_hash):
                raise ValueError(f"{Fore.RED}Некорректный формат API HASH! Должно быть 32 символа (a-z, 0-9)")
                
            return int(api_id), api_hash
        except ValueError as e:
            print(f"\n{Fore.RED}⚠️ Ошибка: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Пожалуйста, попробуйте еще раз...\n")

def load_or_create_api_config():
    """Загрузка или создание конфигурации API"""
    if os.path.exists(API_CONFIG_FILE):
        try:
            with open(API_CONFIG_FILE, "r") as f:
                config = json.load(f)
                print(f"{Fore.GREEN}✅ Найдена сохраненная конфигурация API{Style.RESET_ALL}")
                return config["api_id"], config["api_hash"]
        except Exception as e:
            logger.error(f"Ошибка чтения API конфига: {e}")
    
    print(f"\n{Fore.RED}⚠️ API конфигурация не найдена!{Style.RESET_ALL}")
    api_id, api_hash = get_api_credentials()
    
    # Сохраняем конфиг
    with open(API_CONFIG_FILE, "w") as f:
        json.dump({"api_id": api_id, "api_hash": api_hash}, f)
        print(f"\n{Fore.GREEN}✅ API данные успешно сохранены в {API_CONFIG_FILE}{Style.RESET_ALL}")
    
    return api_id, api_hash

def load_settings():
    """Загрузка настроек бота"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                loaded_settings = json.load(f)
                print(f"{Fore.GREEN}✅ Настройки бота загружены{Style.RESET_ALL}")
                return {**DEFAULT_SETTINGS, **loaded_settings}
        except Exception as e:
            logger.error(f"Ошибка загрузки настроек: {e}")
            return DEFAULT_SETTINGS
    print(f"{Fore.YELLOW}⚠️ Файл настроек не найден, используются настройки по умолчанию{Style.RESET_ALL}")
    return DEFAULT_SETTINGS

def save_settings(settings):
    """Сохранение настроек бота"""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        logger.error(f"Ошибка сохранения настроек: {e}")

def print_welcome_message(api_id):
    """Печать приветственного сообщения"""
    print_header("КОНФИГУРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")
    
    print(f"{Fore.YELLOW}┌─{Fore.CYAN} API ID: {Fore.MAGENTA}{api_id}")
    print(f"{Fore.YELLOW}├─{Fore.CYAN} Префиксы команд: {Fore.MAGENTA}{', '.join(COMMAND_PREFIXES)}")
    print(f"{Fore.YELLOW}├─{Fore.CYAN} Папки плагинов: {Fore.MAGENTA}plugin/, plugin_sist/")
    print(f"{Fore.YELLOW}├─{Fore.CYAN} Логирование: {Fore.MAGENTA}{'ВКЛЮЧЕНО' if settings.get('console_logging', True) else 'ВЫКЛЮЧЕНО'}")
    print(f"{Fore.YELLOW}└─{Fore.CYAN} Временная зона: {Fore.MAGENTA}{settings.get('time_timezone', 'UTC+3')}")
    
    print(f"\n{Style.BRIGHT}{Fore.GREEN}🚀 Бот запущен! Используйте Ctrl+C для остановки.{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.BLUE}💫 Добро пожаловать в COSMO UB - лучший терминальный юзербот!{Style.RESET_ALL}\n")

def load_commands():
    """Загрузка команд из плагинов"""
    commands = {}
    # Загрузка из plugin
    for filename in os.listdir("plugin"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                module_name = filename[:-3]
                module = __import__(f"plugin.{module_name}", fromlist=[module_name])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
                    logger.info(f"Команда '{module.command}' загружена из plugin/{filename}")
            except Exception as e:
                logger.error(f"Ошибка загрузки команды plugin/{filename}: {e}")
    
    # Загрузка из plugin_sist
    for filename in os.listdir("plugin_sist"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                module_name = filename[:-3]
                module = __import__(f"plugin_sist.{module_name}", fromlist=[module_name])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
                    logger.info(f"Системная команда '{module.command}' загружена из plugin_sist/{filename}")
            except Exception as e:
                logger.error(f"Ошибка загрузки системной команды plugin_sist/{filename}: {e}")
    return commands

# Основной код
if __name__ == "__main__":
    print_banner()
    
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Telegram UserBot')
    parser.add_argument('--reconfig', action='store_true', help='Переконфигурировать API данные')
    args = parser.parse_args()
    
    # Принудительная переконфигурация при необходимости
    if args.reconfig and os.path.exists(API_CONFIG_FILE):
        os.remove(API_CONFIG_FILE)
        print(f"\n{Fore.YELLOW}⚠️ Конфигурация API удалена. Запустите повторно для настройки.{Style.RESET_ALL}")
        sys.exit(0)
    
    # Загрузка настроек API
    api_id, api_hash = load_or_create_api_config()
    
    # Загрузка настроек бота
    settings = load_settings()
    
    # Отключение логирования в консоль если нужно
    if not settings.get("console_logging", True):
        logging.getLogger().handlers = []
        logger.info("Консольное логирование отключено")
    
    # Создаём папки для плагинов
    os.makedirs("plugin", exist_ok=True)
    os.makedirs("plugin_sist", exist_ok=True)
    
    # Создаем клиент Pyrogram (исправленная версия без недопустимых параметров)
    app = Client(
    "cosmo_ub",
    api_id=api_id,
    api_hash=api_hash,
    workers=2,  # Уменьшаем количество workers для мобильных устройств
    sleep_threshold=30,  # Более агрессивный таймаут
    no_updates=True,  # Отключаем получение обновлений для экономии трафика
    ipv6=False,  # Принудительно используем IPv4
    proxy=None,  # Явно отключаем прокси, если не используется
    test_mode=False,  # Режим продакшена
    app_version="Cosmo UB 2.0",
    device_model="Termux",
    system_version="Android"
)
    
    # Загрузка команд
    commands = load_commands()
    
    # Обработчик сообщений
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
                logger.info(f"Выполнение: {command}")
                start_time = time.time()
                try:
                    await commands[command](client, message, args, settings)
                    logger.info(f"Команда '{command}' выполнена за {time.time() - start_time:.2f}с")
                except Exception as e:
                    logger.error(f"Ошибка в {command}: {e}")
                    await message.reply(f"""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Ошибка выполнения!
├─▶ 🐞 {str(e)}
╰───⋞🌌 Powered by Cosmo UB 🌌⋟
""")
            else:
                logger.warning(f"Неизвестная команда: {command}")
                await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ Неизвестная команда!
├─▶ 🔍 {command}
╰───⋞🌌 Powered by Cosmo UB 🌌⋟
""")

        except (PeerIdInvalid, ChannelInvalid) as e:
            logger.warning(f"Неверный peer/канал: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
    
    # Печать приветственного сообщения
    print_welcome_message(api_id)
    
    # Запуск бота
    logger.info("Запуск COSMO UB...")
    app.run()