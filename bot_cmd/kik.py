from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "kik"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not message.chat.type in ["group", "supergroup"]:
        await message.reply("❌ Эта команда только для групп!")
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif args:
        try:
            user = await client.get_users(args.strip('@'))
        except:
            await message.reply("❌ Пользователь не найден")
            return
    else:
        await message.reply("❌ Укажите @username или ответьте на сообщение")
        return

    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"👢 Пользователь {user.first_name} исключен!")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")
