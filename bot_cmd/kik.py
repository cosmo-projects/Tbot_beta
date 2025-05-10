from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError

command = "kik"

async def handler(client: Client, message: Message, args: str, settings: dict):
    # Проверка типа чата
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply("🚫 Команда доступна только в группах и супергруппах!")
        return

    # Проверка прав администратора
    try:
        me = await client.get_chat_member(message.chat.id, "me")
        if not me.privileges or not me.privileges.can_restrict_members:
            await message.reply("🔒 У меня нет прав на исключение участников!")
            return
    except Exception as e:
        await message.reply(f"⚠️ Ошибка проверки прав: {e}")
        return

    # Получение цели
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        elif args:
            user = await client.get_users(args.strip('@'))
        else:
            await message.reply("ℹ️ Ответьте на сообщение или укажите @username")
            return

        # Исключение пользователя
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"👋 {user.mention} был исключён из чата!")
        
    except RPCError as e:
        await message.reply(f"❌ Ошибка Telegram: {e}")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {e}")
