from aiogram import types, F
from aiogram.types import Message
from config import FILMS_CHAT
from services.post_storage import add_post_to_file
import logging

def register_channel_handlers(dp):
    @dp.channel_post(F.chat.id == FILMS_CHAT)
    async def handle_channel_post(post: types.Message):
        description = post.caption.split('\n')[0].strip() if post.caption else "Без описания"
        logging.info(f"Получено сообщение из канала: {description}")
        add_post_to_file(description, post.chat.id, post.message_id)
