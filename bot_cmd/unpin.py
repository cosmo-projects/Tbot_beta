from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "unpin"

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        await client.unpin_chat_message(message.chat.id)
        await message.reply("📌 Сообщение откреплено!")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")
