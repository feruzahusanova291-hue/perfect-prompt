from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import PromptStates
from keyboards.keyboards import get_cancel_keyboard, get_prompt_actions_keyboard
from services.prompt_engine import prompt_engine
from services.ai_service import ai_service
from utils.helpers import send_smart_message

router = Router(name="translate_router")


@router.message(F.text == "🔄 Tarjima")
async def choose_translate(message: Message, state: FSMContext) -> None:
    """Professional prompt tarjimasi rejimini yoqish."""
    await state.set_state(PromptStates.waiting_for_translate_text)
    text = (
        "🔄 **PROFESSIONAL PROMPT TARJIMASI**\n\n"
        "Oddiy so'zma-so'z tarjima emas, AI generatorlar (Midjourney, Flux, Kling, Runway) "
        "uchun eng to'g'ri fotografik va texnik atamalardan foydalangan holda professional tarjima qilinadi.\n\n"
        "✍️ **O'zbekcha yoki Inglizcha promptingizni yuboring:**"
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")


@router.message(PromptStates.waiting_for_translate_text, F.text)
async def process_translate(message: Message, state: FSMContext) -> None:
    """Promptni tarjima qilish."""
    user_text = message.text.strip()
    if len(user_text) < 2:
        await message.answer("⚠️ Iltimos, prompt matnini to'liq yuboring.")
        return

    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    lang = user_data.get("language", "uz")

    wait_msg = await message.answer("⏳ *Professional prompt tarjimasi shakllantirilmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode="translate",
        user_text=user_text,
        language=lang,
    )

    prompt_engine.set_last_prompt(user_id, prompt=user_text, mode="translate", result=result)
    await state.clear()

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(message, result, reply_markup=get_prompt_actions_keyboard())
