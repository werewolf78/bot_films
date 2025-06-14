
from aiogram import F
from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus
from config import FILMS_CHAT, TESTA
from handlers.groups import search_and_reply

def register_private_handlers(dp, bot):
    @dp.message(F.chat.type == "private")
    async def private_search(message: Message):
        user_id = message.from_user.id

        # Проверка членства хотя бы в одной из групп
        is_member = False
        for group_id in [FILMS_CHAT, TESTA]:
            try:
                member = await bot.get_chat_member(group_id, user_id)
                if member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    is_member = True
                    break
            except Exception:
                continue  # если бот не может получить данные — пропускаем

        if not is_member:
            await message.answer("⛔ Вы не состоите ни в одной из групп, где я работаю.")
            return

        title = message.text.strip()
        if not title:
            await message.answer("Пожалуйста, напишите название фильма или сериала.")
            return

        await message.answer(f"🔍 Ищу '{title}'...")
        await search_and_reply(message, title)
