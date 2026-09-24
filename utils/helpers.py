import logging
from aiogram.types import Message, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4000


async def send_smart_message(
    message: Message,
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "Markdown",
) -> None:
    """Xabarni xavfsiz va uzun bo'lsa bo'laklab yuborish."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        try:
            await message.answer(text, parse_mode=parse_mode, reply_markup=reply_markup)
            return
        except Exception as e:
            logger.warning(f"Markdown formatida yuborishda xatolik ({e}), oddiy matnda yuborilmoqda.")
            try:
                await message.answer(text, parse_mode=None, reply_markup=reply_markup)
                return
            except Exception as e2:
                logger.error(f"Xabar yuborishda xatolik: {e2}")
                return

    # 4000 belgidan uzun bo'lsa bo'laklarga ajratish
    chunks = []
    current_text = text
    while len(current_text) > MAX_MESSAGE_LENGTH:
        split_pos = current_text.rfind("\n\n", 0, MAX_MESSAGE_LENGTH)
        if split_pos == -1:
            split_pos = current_text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if split_pos == -1:
            split_pos = MAX_MESSAGE_LENGTH

        chunks.append(current_text[:split_pos].strip())
        current_text = current_text[split_pos:].strip()

    if current_text:
        chunks.append(current_text)

    for i, chunk in enumerate(chunks):
        is_last = i == len(chunks) - 1
        markup = reply_markup if is_last else None
        try:
            await message.answer(chunk, parse_mode=parse_mode, reply_markup=markup)
        except Exception:
            await message.answer(chunk, parse_mode=None, reply_markup=markup)
