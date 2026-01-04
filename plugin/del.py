from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError, MessageDeleteForbidden

command = "del"

async def handler(client: Client, message: Message, args: str, settings: dict):
    """
    Удаление сообщений:
    1. .del - удалить сообщение, на которое ответили (реплай)
    2. .del <число> - удалить указанное количество сообщений от себя
    3. .del all - удалить все сообщения от себя в этом чате (макс 100)
    """
    
    try:
        if args:
            # Обработка аргументов
            if args.lower() == "all":
                # Удаляем все сообщения от себя (ограничение Telegram API - 100 сообщений)
                deleted_count = 0
                async for msg in client.search_messages(
                    chat_id=message.chat.id,
                    from_user="me",
                    limit=100
                ):
                    try:
                        await client.delete_messages(message.chat.id, msg.id)
                        deleted_count += 1
                    except:
                        continue
                
                response = f"""
╭───⋞⚙️ DELETE INFO ⚙️⋟───╮
├─▶ ✅ Удалено сообщений: {deleted_count}
├─▶ 🗑️ (из последних 100 ваших сообщений)
╰───⋞🌌 Powered by Cosmo 🌌⋟
"""
                await message.reply(response)
                return
            
            # Удаление N сообщений от себя
            try:
                count = int(args)
                if count <= 0:
                    await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Число должно быть положительным!
├─▶ 💡 Пример: .del 5
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                    return
                
                if count > 100:
                    count = 100  # Ограничение Telegram API
                    await message.reply("""
╭───⋞⚙️ SYSTEM WARNING ⚙️⋟───╮
├─▶ ⚠️ Максимальное количество - 100
├─▶ 📉 Будет удалено 100 сообщений
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                
                # Получаем последние N сообщений от себя
                message_ids = []
                async for msg in client.search_messages(
                    chat_id=message.chat.id,
                    from_user="me",
                    limit=count
                ):
                    message_ids.append(msg.id)
                
                if not message_ids:
                    await message.reply("""
╭───⋞⚙️ DELETE INFO ⚙️⋟───╮
├─▶ ℹ️ Не найдено ваших сообщений
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                    return
                
                # Удаляем пачками по 100 (ограничение Telegram API)
                for i in range(0, len(message_ids), 100):
                    batch = message_ids[i:i+100]
                    await client.delete_messages(message.chat.id, batch)
                
                response = f"""
╭───⋞⚙️ DELETE INFO ⚙️⋟───╮
├─▶ ✅ Удалено сообщений: {len(message_ids)}
╰───⋞🌌 Powered by Cosmo 🌌⋟
"""
                await message.reply(response)
                return
                
            except ValueError:
                await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Неверный аргумент!
├─▶ 💡 Используйте:
├─▶ .del - удалить реплай
├─▶ .del <число> - удалить N ваших сообщений
├─▶ .del all - удалить все ваши сообщения
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
                return
        
        # Режим по умолчанию - удаление реплая
        if not message.reply_to_message:
            await message.reply("""
╭───⋞⚙️ DELETE USAGE ⚙️⋟───╮
├─▶ 💡 Использование команды:
├─▶ 
├─▶ 🗑️ .del - удалить сообщение (реплай)
├─▶ 🔢 .del <число> - удалить N ваших сообщений
├─▶ 🧹 .del all - удалить все ваши сообщения (до 100)
├─▶ 
├─▶ ❗ Без аргумента нужен реплай!
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            return
        
        # Удаляем сообщение, на которое ответили
        try:
            # Удаляем оба сообщения: реплай и команду
            await client.delete_messages(
                message.chat.id,
                [message.reply_to_message.id, message.id]
            )
            
        except MessageDeleteForbidden:
            # Если нельзя удалить чужие сообщения, удаляем только своё
            await message.delete()
            await message.reply("""
╭───⋞⚙️ DELETE WARNING ⚙️⋟───╮
├─▶ ⚠️ Не могу удалить чужое сообщение!
├─▶ ✅ Ваша команда удалена
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
            
    except Exception as e:
        error_msg = str(e)
        if "MESSAGE_DELETE_FORBIDDEN" in error_msg:
            await message.reply("""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Нет прав на удаление!
├─▶ ⚠️ Вам нужны права администратора
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")
        else:
            await message.reply(f"""
╭───⋞⚙️ SYSTEM ERROR ⚙️⋟───╮
├─▶ ❗ Произошла ошибка!
├─▶ ⚠️ Ошибка: {error_msg[:50]}
╰───⋞🌌 Powered by Cosmo 🌌⋟
""")