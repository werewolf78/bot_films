

from services.db import add_known_user, remove_known_user
from aiogram.types import ChatMemberUpdated
from aiogram.enums.chat_member_status import ChatMemberStatus
from services.db import remove_known_user
from aiogram import types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from config import TESTA, FILMS_CHAT
from services.post_storage import find_post_lines_by_title
import re
import logging

# Настройка логгирования
logger = logging.getLogger(__name__)

# ID групп, в которых работает бот
group_chats = [FILMS_CHAT, TESTA]

def register_group_handlers(dp, bot):
    # Обработка колбэков от inline-кнопок
    @dp.callback_query(F.data.startswith(("search:", "thanks")))
    async def handle_callback(callback: CallbackQuery):
        try:
            if callback.data == "thanks":
                await callback.message.edit_text("❤️")
                await callback.answer()
            elif callback.data.startswith("search:"):
                title = callback.data[7:]
                await callback.message.edit_text(f"🔍 Ищу '{title}'...")
                await search_and_reply(callback.message, title)
                await callback.answer()
        except Exception as e:
            logger.error(f"Ошибка при обработке callback: {e}")
            await callback.answer("❌ Произошла ошибка")

    # Обработка сообщений в группах
    @dp.message(F.chat.type.in_({"group", "supergroup"}) & F.chat.id.in_(group_chats))
    async def handle_group_message(message: Message):
        await add_known_user(message.from_user.id)
        try:
            if not message.text:
                return

            text = message.text.lower()

            # Ответ на сообщение бота
            if message.reply_to_message and message.reply_to_message.from_user.id == message.bot.id:
                title = message.text.strip()
                if not title:
                    await message.reply("❌ Пожалуйста, укажите название фильма или сериала.")
                    return

                gratitude_words = ["спасибо", "благодарю", "спс", "thx", "thanks", "thank you", "пасибо"]
                if any(word in text for word in gratitude_words):
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🎬 Вопрос", callback_data=f"search:{title}"),
                            InlineKeyboardButton(text="❤️ Благодарность", callback_data="thanks")
                        ]
                    ])
                    await message.reply("🤔 Это вопрос или благодарность?", reply_markup=keyboard)
                    return

                await search_and_reply(message, title)
                return

            # Если сообщение содержит благодарность
            gratitude_words = ["спасибо", "благодарю", "спс", "thx", "thanks", "thank you", "пасибо"]
            if any(word in text for word in gratitude_words):
                await message.reply("❤️")
                return

            # Триггерные слова для предложения помощи
            trigger_words = ["фильм", "сериал", "кино", "фильмы", "сериалы", "бот"]
            if any(word in text for word in trigger_words):
                await message.reply(
                    "🎬 Приветствую! Я могу помочь найти фильм или сериал.\n"
                    "📝 Ответьте на это сообщение названием того, что ищете."
                )
                return

        except TelegramBadRequest as e:
            logger.error(f"Ошибка Telegram API: {e}")
            await message.reply("❌ Ошибка при отправке сообщения. Попробуйте еще раз.")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            await message.reply("❌ Произошла ошибка. Попробуйте позже.")

async def search_and_reply(message: Message, title: str):
    """
    Поиск контента и отправка результатов
    """
    try:
        full_lines = find_post_lines_by_title(title)

        if not full_lines:
            await message.reply(
                f"😔 К сожалению, '{title}' не найдено в каталоге.\n"
                "Попробуйте другое название или проверьте правильность написания."
            )
            return

        response = []
        processed_count = 0

        for line in full_lines:
            try:
                match = re.search(r'^(.*?):\s+(https://t\.me/c/\d+/\d+(\?[\w=&]*)?)$', line.strip())
                if match:
                    description, url = match.group(1), match.group(2)
                    description_clean = escape_markdown_v2(description.strip())
                    if is_valid_telegram_url(url):
                        response.append(f"[{description_clean}]({url})")
                        processed_count += 1
                    else:
                        logger.warning(f"Неверный формат ссылки: {url}")
                else:
                    logger.warning(f"Строка не соответствует шаблону: {line}")
            except Exception as e:
                logger.error(f"Ошибка при обработке строки: {line}, ошибка: {e}")
                continue

        if response:
            response_text = "\n".join(response)
            if len(response_text) > 4000:
                chunks = split_response(response, 4000)
                for i, chunk in enumerate(chunks):
                    chunk_text = "\n".join(chunk)
                    if i == 0:
                        await message.reply(
                            f"🎯 Найдено {processed_count} результатов для '{title}':\n\n{chunk_text}",
                            parse_mode="MarkdownV2"
                        )
                    else:
                        await message.answer(chunk_text, parse_mode="MarkdownV2")
            else:
                await message.reply(
                    f"🎯 Найдено {processed_count} результатов для '{title}':\n\n{response_text}",
                    parse_mode="MarkdownV2"
                )
        else:
            await message.reply(
                f"⚠️ Найдены записи для '{title}', но не удалось извлечь корректные ссылки.\n"
                "Обратитесь к администратору."
            )
    except Exception as e:
        logger.error(f"Ошибка в search_and_reply: {e}")
        await message.reply("❌ Произошла ошибка при поиске.")

def escape_markdown_v2(text: str) -> str:
    """
    Экранирование спецсимволов для MarkdownV2
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def is_valid_telegram_url(url: str) -> bool:
    """
    Проверка корректности ссылки Telegram
    """
    pattern = r'^https://t\.me/c/\d+/\d+(\?[\w=&]*)?$'
    return bool(re.match(pattern, url))

def split_response(response_list: list, max_length: int) -> list:
    """
    Разделение длинного ответа на части, чтобы укладываться в лимит Telegram
    """
    chunks = []
    current_chunk = []
    current_length = 0

    for item in response_list:
        item_length = len(item) + 1  # +1 за перенос строки
        if current_length + item_length > max_length and current_chunk:
            chunks.append(current_chunk)
            current_chunk = [item]
            current_length = item_length
        else:
            current_chunk.append(item)
            current_length += item_length

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


    @dp.chat_member()
    async def handle_member_leave(event: ChatMemberUpdated):
        if event.chat.id in [FILMS_CHAT, TESTA]:
            if event.new_chat_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                await remove_known_user(event.from_user.id)


