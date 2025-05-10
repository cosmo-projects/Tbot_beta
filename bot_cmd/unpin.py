from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "unpin"

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        # Получаем текущее закрепленное сообщение
        chat = await client.get_chat(message.chat.id)
        
        if not chat.pinned_message:
            await message.reply("ℹ️ В этом чате нет закрепленных сообщений")
            return
            
        # Пробуем открепить все сообщения
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply("📌 Все сообщения откреплены!")
        
    except RPCError as e:
        if "MESSAGE_ID_INVALID" in str(e):
            # Если возникает ошибка неверного ID, пробуем альтернативный метод
            try:
                await client.unpin_all_chat_messages(message.chat.id)
                await message.reply("📌 Сообщения откреплены (исправлено через unpin_all)!")
            except Exception as e2:
                await message.reply(f"⚠️ Ошибка при откреплении: {str(e2)}")
        else:
            await message.reply(f"⚠️ Ошибка: {str(e)}")
    except Exception as e:
        await message.reply(f"⚠️ Неизвестная ошибка: {str(e)}")
