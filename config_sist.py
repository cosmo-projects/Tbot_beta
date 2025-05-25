# Основные настройки системы
COMMAND_PREFIXES = [".l", "azi", ".tlp"]
DEFAULT_SETTINGS = {
    "time_timezone": "UTC+3",
    "alias_settings": {
        "require_prefix": True,  # Требовать префикс для алиасов
        "allowed_prefixes": [".l", "azi", ".tlp"]  # Разрешенные префиксы
    },
    "aliases": {
        "fix": "pin"  # Пример алиаса по умолчанию
    }
}
