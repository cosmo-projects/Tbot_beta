from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "del"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not message.reply_to_message:
        await message.reply("❌ Ответьте на сообщение для удаления")
        return

    try:
        await client.delete_messages(
            message.chat.id,
            message.reply_to_message.id
        )
        await message.reply("🗑️ Сообщение удалено!")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")
