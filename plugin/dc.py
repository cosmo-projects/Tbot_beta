from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError, FloodWait
import asyncio

# ============================================
# СПИСОК КАНАЛОВ, КОТОРЫЕ НЕ НАДО УДАЛЯТЬ
# ============================================
PINNED_CHANNELS = [
    "fpfpfpfpffp",  # твой канал (username без @)
    # "durov",       # пример другого канала
    # -1001234567890, # пример ID канала
]

command = "leave_channels"

async def handler(client: Client, message: Message, args: str, settings: dict):
    status_msg = await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ 🔍 Сканирую каналы...
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
    
    try:
        left_count = 0
        skipped_count = 0
        error_count = 0
        
        async for dialog in client.get_dialogs():
            # Проверяем только каналы
            if dialog.chat.type == "channel":
                chat_title = dialog.chat.title or "Без названия"
                chat_username = dialog.chat.username
                chat_id = dialog.chat.id
                
                # Проверяем, нужно ли сохранить канал
                should_keep = False
                
                # Проверка по username
                if chat_username and chat_username in PINNED_CHANNELS:
                    should_keep = True
                
                # Проверка по ID
                if chat_id in PINNED_CHANNELS:
                    should_keep = True
                
                if should_keep:
                    skipped_count += 1
                    await status_msg.edit_text(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ 📌 ОСТАВЛЯЮ: {chat_title[:30]}
├─▶ ✅ Выйду из: {left_count}
├─▶ 📌 Оставлю: {skipped_count}
├─▶ ❌ Ошибок: {error_count}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                    continue
                
                try:
                    # Выходим из канала
                    await client.leave_chat(chat_id)
                    left_count += 1
                    
                    await status_msg.edit_text(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ✅ ВЫШЕЛ ИЗ: {chat_title[:30]}
├─▶ ✅ Всего вышли: {left_count}
├─▶ 📌 Оставили: {skipped_count}
├─▶ ❌ Ошибок: {error_count}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                    
                    # Задержка чтобы не заблокировали
                    await asyncio.sleep(1.5)
                    
                except FloodWait as e:
                    wait_time = e.value
                    await status_msg.edit_text(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ⏳ Flood wait {wait_time}с
├─▶ ✅ Успели выйти: {left_count}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                    await asyncio.sleep(wait_time)
                    
                except RPCError as e:
                    error_count += 1
                    await status_msg.edit_text(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❌ Ошибка в канале
├─▶ ⚠️ {str(e)[:50]}
├─▶ ✅ Вышли: {left_count}
├─▶ 📌 Оставили: {skipped_count}
├─▶ ❌ Ошибок: {error_count}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        
        # Финальный отчет
        await status_msg.edit_text(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ✅ ВСЕ ГОТОВО!
├─▶ 
├─▶ 🚪 Вышли из: {left_count} каналов
├─▶ 📌 Оставили: {skipped_count} каналов
├─▶ ❌ Ошибок: {error_count}
├─▶ 
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        
    except Exception as e:
        await status_msg.edit_text(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
├─▶ ❗ КРИТИЧЕСКАЯ ОШИБКА!
├─▶ ⚠️ {str(e)}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
