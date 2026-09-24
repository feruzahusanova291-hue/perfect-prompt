from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import PromptStates
from keyboards.keyboards import get_cancel_keyboard, get_prompt_actions_keyboard
from services.prompt_engine import prompt_engine
from services.ai_service import ai_service
from utils.helpers import send_smart_message

router = Router(name="image_router")


@router.message(F.text == "🖼️ Rasm prompti")
async def choose_image_prompt(message: Message, state: FSMContext) -> None:
    """Rasm prompti rejimini yoqish."""
    await state.set_state(PromptStates.waiting_for_image_idea)
    user_data = prompt_engine.get_user_data(message.from_user.id)
    platform = user_data.get("platform", "Universal")

    text = (
        "🖼️ **RASM UCHUN PROMPT GENERATORI**\n\n"
        f"🎯 Tanlangan platforma: `{platform}`\n\n"
        "✍️ **G‘oyangizni yoki xomaki promptingizni yuboring:**\n"
        "*(Masalan: 'Tungi yomg'irli ko'chada soyabon ushlab turgan qiz' yoki 'Futuristik kiberpank avtomobil')*"
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")


@router.message(PromptStates.waiting_for_image_idea, F.text)
async def process_image_idea(message: Message, state: FSMContext) -> None:
    """Foydalanuvchi g'oyasini qabul qilib, professional rasm prompti yaratish."""
    user_idea = message.text.strip()
    if len(user_idea) < 2:
        await message.answer("⚠️ Iltimos, batafsilroq g'oya yozing.")
        return

    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    wait_msg = await message.answer("⏳ *Prompt ustida professional tahlil va generatsiya ketmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode="image",
        user_text=user_idea,
        platform=platform,
        language=lang,
    )

    # Oxirgi promptni saqlash
    prompt_engine.set_last_prompt(user_id, prompt=user_idea, mode="image", result=result)
    await state.clear()

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(message, result, reply_markup=get_prompt_actions_keyboard())
