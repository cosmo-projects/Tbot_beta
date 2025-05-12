from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "del"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not message.reply_to_message:
        await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
│
├─▶ ❗ Произошла ошибка!
├─▶ ❌ Ответьте на сообщение, которое нужно удалить
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
        return

    try:
        await client.delete_messages(
            message.chat.id,
            message.reply_to_message.id
        )
        await message.reply("""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
│
├─▶ 🗑️ Сообщение успешно удалено!
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
    except Exception as e:
        await message.reply(f"""
╭───⋞⚙️ SYSTEM INFO ⚙️⋟───╮
│
├─▶ ❗ Произошла ошибка!
├─▶ ⚠️ Ошибка: {str(e)}
│
╰───⋞🌌 Powered by Cosmo 🌌⋟───╯
""")
