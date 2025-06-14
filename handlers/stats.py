from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from services.db import get_users_count
from utils import is_admin

router = Router()

@router.message(Command("stats"), F.chat.type == "private")
async def stats_command(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("⛔️ Команда доступна только администраторам.")

    count = await get_users_count()
    await message.answer(f"📊 Всего пользователей: {count}")