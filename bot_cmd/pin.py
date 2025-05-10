from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "pin"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not message.reply_to_message:
        await message.reply("❌ Ответьте на сообщение для закрепления")
        return

    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.id,
            disable_notification=True
        )
        await message.reply("📌 Сообщение закреплено!")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")
