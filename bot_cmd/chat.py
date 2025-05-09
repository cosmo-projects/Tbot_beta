from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError

commands = ["kik", "add", "pin", "unpin", "del"]

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        if not message.text:
            return
            
        cmd = message.text.split()[0].lower().replace(('.l', 'azi', '.tlp')[0], '')
        
        if cmd == "kik":
            await kick_user(client, message)
        elif cmd == "add":
            await add_user(client, message)
        elif cmd == "pin":
            await pin_message(client, message)
        elif cmd == "unpin":
            await unpin_message(client, message)
        elif cmd == "del":
            await delete_message(client, message)
            
    except RPCError as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")
    except Exception as e:
        await message.reply(f"⚠️ Неизвестная ошибка: {str(e)}")

async def get_target_user(client: Client, message: Message):
    # Для команд с reply
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
        
    # Для команд с @username
    if len(message.text.split()) > 1:
        username = message.text.split()[1].strip('@')
        try:
            return await client.get_users(username)
        except:
            return None
    return None

async def kick_user(client: Client, message: Message):
    if not message.chat.type in ["group", "supergroup"]:
        await message.reply("❌ Эта команда только для групп!")
        return

    user = await get_target_user(client, message)
    if not user:
        await message.reply("❌ Укажите @username или ответьте на сообщение")
        return

    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"👢 Пользователь {user.first_name} исключен!")
    except Exception as e:
        await message.reply(f"⚠️ Не удалось исключить: {str(e)}")

async def add_user(client: Client, message: Message):
    if not message.chat.type in ["group", "supergroup"]:
        await message.reply("❌ Эта команда только для групп!")
        return

    user = await get_target_user(client, message)
    if not user:
        await message.reply("❌ Укажите @username или ответьте на сообщение")
        return

    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply(f"✅ Пользователь {user.first_name} добавлен!")
    except Exception as e:
        await message.reply(f"⚠️ Не удалось добавить: {str(e)}")

async def pin_message(client: Client, message: Message):
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
        await message.reply(f"⚠️ Не удалось закрепить: {str(e)}")

async def unpin_message(client: Client, message: Message):
    try:
        await client.unpin_chat_message(message.chat.id)
        await message.reply("📌 Сообщение откреплено!")
    except Exception as e:
        await message.reply(f"⚠️ Не удалось открепить: {str(e)}")

async def delete_message(client: Client, message: Message):
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
        await message.reply(f"⚠️ Не удалось удалить: {str(e)}")
