from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

command = "add"

async def handler(client: Client, message: Message, args: str, settings: dict):
    # Проверяем, что команда вызвана в группе/супергруппе
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("❌ Эта команда работает только в группах и супергруппах!")
        return

    # Проверяем права бота
    try:
        me = await client.get_chat_member(message.chat.id, "me")
        if not me.can_invite_users:
            await message.reply("❌ У меня нет прав на добавление участников!")
            return
    except Exception as e:
        await message.reply(f"⚠️ Ошибка проверки прав: {str(e)}")
        return

    # Получаем целевого пользователя
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif args:
        try:
            user = await client.get_users(args.strip('@'))
        except:
            await message.reply("❌ Пользователь не найден")
            return
    else:
        await message.reply("❌ Укажите @username или ответьте на сообщение пользователя")
        return

    # Пытаемся добавить
    try:
        await client.unban_chat_member(
            chat_id=message.chat.id,
            user_id=user.id
        )
        await message.reply(f"✅ Пользователь {user.mention} был добавлен!")
    except Exception as e:
        await message.reply(f"⚠️ Не удалось добавить: {str(e)}")
