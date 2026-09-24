import io
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import PromptStates
from keyboards.keyboards import get_cancel_keyboard, get_prompt_actions_keyboard
from services.prompt_engine import prompt_engine
from services.ai_service import ai_service
from utils.helpers import send_smart_message

router = Router(name="video_router")


@router.message(F.text == "🎬 Video prompti")
async def choose_video_prompt(message: Message, state: FSMContext) -> None:
    """Video prompti rejimini yoqish."""
    await state.set_state(PromptStates.waiting_for_video_idea)
    user_data = prompt_engine.get_user_data(message.from_user.id)
    platform = user_data.get("platform", "Universal")

    text = (
        "🎬 **VIDEO UCHUN PROMPT GENERATORI**\n\n"
        f"🎯 Tanlangan platforma: `{platform}`\n\n"
        "✍️ **Video g‘oyangizni yozing yoki rasm yuboring (Image-to-Video):**\n\n"
        "• *Oddiy matn yuborsangiz* — kamera harakati, fizika, vaqt segmentlari bilan to'liq video prompt yaratiladi.\n"
        "• *Rasm yuborsangiz* — asl qiyofa va fonni saqlagan holda harakat ssenariysi tuziladi."
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")


@router.message(PromptStates.waiting_for_video_idea, F.text)
async def process_video_text(message: Message, state: FSMContext) -> None:
    """Matnli video g'oyasini qayta ishlash."""
    user_idea = message.text.strip()
    if len(user_idea) < 2:
        await message.answer("⚠️ Iltimos, video g'oyasini batafsilroq yozing.")
        return

    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    wait_msg = await message.answer(
        "⏳ *Video harakati, kamera trayektoriyasi va fizika tahlil qilinmoqda...*",
        parse_mode="Markdown",
    )

    result = await ai_service.generate_prompt(
        mode="video",
        user_text=user_idea,
        platform=platform,
        language=lang,
    )

    prompt_engine.set_last_prompt(user_id, prompt=user_idea, mode="video", result=result)
    await state.clear()

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(message, result, reply_markup=get_prompt_actions_keyboard())


@router.message(PromptStates.waiting_for_video_idea, F.photo)
async def process_image_to_video(message: Message, state: FSMContext, bot: Bot) -> None:
    """Rasmli Image-to-Video g'oyasini qayta ishlash."""
    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    caption = message.caption or "Ushbu rasm asosida tabiiy va silliq kinematografik harakat yarating."

    wait_msg = await message.answer(
        "⏳ *Rasm tahlil qilinmoqda va Image-to-Video uzluksiz prompti yaratilmoqda...*",
        parse_mode="Markdown",
    )

    # Eng sifatli rasm o'lchamini olish
    photo = message.photo[-1]
    image_bytes = None
    try:
        file = await bot.get_file(photo.file_id)
        buffer = io.BytesIO()
        await bot.download_file(file.file_path, destination=buffer)
        image_bytes = buffer.getvalue()
    except Exception as e:
        await message.answer(f"⚠️ Rasmni yuklab olishda muammo bo'ldi: {e}")

    result = await ai_service.generate_prompt(
        mode="video",
        user_text=caption,
        platform=platform,
        language=lang,
        image_bytes=image_bytes,
    )

    prompt_engine.set_last_prompt(user_id, prompt=caption, mode="video", result=result)
    await state.clear()

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(message, result, reply_markup=get_prompt_actions_keyboard())
