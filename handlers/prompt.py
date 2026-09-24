from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from handlers.states import PromptStates
from keyboards.keyboards import (
    get_cancel_keyboard,
    get_prompt_actions_keyboard,
    get_platform_selection_keyboard,
    get_main_menu_keyboard,
)
from services.prompt_engine import prompt_engine
from services.ai_service import ai_service
from utils.helpers import send_smart_message

router = Router(name="prompt_router")


# ==========================================
# 🛠️ PROMPTNI TUZATISH
# ==========================================
@router.message(F.text == "🛠️ Promptni tuzatish")
async def choose_fix_prompt(message: Message, state: FSMContext) -> None:
    """Promptni tuzatish rejimini yoqish."""
    await state.set_state(PromptStates.waiting_for_fix_prompt)
    text = (
        "🛠️ **PROMPTNI TAHLIL QILISH VA TUZATISH**\n\n"
        "Xato, tushunarsiz yoki kuchsiz yozilgan promptingizni yuboring.\n"
        "Bot uni tahlil qilib, xatolarini ko'rsatadi va professional darajada qayta yozadi."
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")


@router.message(PromptStates.waiting_for_fix_prompt, F.text)
async def process_fix_prompt(message: Message, state: FSMContext) -> None:
    """Yuborilgan promptni tahlil qilib tuzatish."""
    prompt_text = message.text.strip()
    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    wait_msg = await message.answer("⏳ *Prompt tahlil qilinmoqda va qayta yozilmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode="fix",
        user_text=prompt_text,
        platform=platform,
        language=lang,
    )

    prompt_engine.set_last_prompt(user_id, prompt=prompt_text, mode="fix", result=result)
    await state.clear()

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(message, result, reply_markup=get_prompt_actions_keyboard())


# ==========================================
# 🚀 PROMPTNI KUCHAYTIRISH
# ==========================================
@router.message(F.text == "🚀 Promptni kuchaytirish")
async def choose_enhance_prompt(message: Message, state: FSMContext) -> None:
    """Promptni kuchaytirish rejimini yoqish."""
    await state.set_state(PromptStates.waiting_for_enhance_prompt)
    text = (
        "🚀 **PROMPTNI KUCHAYTIRISH (CREATIVE BOOST)**\n\n"
        "Mavjud promptingizni yuboring. Bot uning asl g'oyasini saqlagan holda "
        "kuchli vizual iyerarxiya, cinematic yorug'lik va professional detallar qo'shadi."
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="Markdown")


@router.message(PromptStates.waiting_for_enhance_prompt, F.text)
async def process_enhance_prompt(message: Message, state: FSMContext) -> None:
    """Yuborilgan promptni kuchaytirish."""
    prompt_text = message.text.strip()
    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    wait_msg = await message.answer("⏳ *Prompt cinematic uslubda kuchaytirilmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode="enhance",
        user_text=prompt_text,
        platform=platform,
        language=lang,
    )

    prompt_engine.set_last_prompt(user_id, prompt=prompt_text, mode="enhance", result=result)
    await state.clear()

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(message, result, reply_markup=get_prompt_actions_keyboard())


# ==========================================
# ⚡ INLINE AMALLAR (NATIJA TAGIDAGI TUGMALAR)
# ==========================================
@router.callback_query(F.data == "act_enhance")
async def callback_enhance_last(callback: CallbackQuery) -> None:
    """Oxirgi hosil qilingan natijani yanada kuchaytirish."""
    await callback.answer("🚀 Kuchaytirilmoqda...")
    user_id = callback.from_user.id
    last_data = prompt_engine.get_last_prompt(user_id)

    if not last_data or not last_data.get("prompt"):
        await callback.message.answer("⚠️ Oxirgi prompt topilmadi. Yangi g'oya yuboring.")
        return

    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    wait_msg = await callback.message.answer("⏳ *Prompt yanada chuqur va cinematic darajada kuchaytirilmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode="enhance",
        user_text=last_data["prompt"],
        platform=platform,
        language=lang,
    )

    prompt_engine.set_last_prompt(user_id, prompt=last_data["prompt"], mode="enhance", result=result)

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(callback.message, result, reply_markup=get_prompt_actions_keyboard())


@router.callback_query(F.data == "act_regenerate")
async def callback_regenerate_last(callback: CallbackQuery) -> None:
    """Oxirgi promptni qaytadan boshqacha variantda yaratish."""
    await callback.answer("🔄 Qayta yaratilmoqda...")
    user_id = callback.from_user.id
    last_data = prompt_engine.get_last_prompt(user_id)

    if not last_data or not last_data.get("prompt"):
        await callback.message.answer("⚠️ Oxirgi prompt topilmadi. Yangi g'oya yuboring.")
        return

    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")
    mode = last_data.get("mode", "image")

    wait_msg = await callback.message.answer("⏳ *Yangi variant generatsiya qilinmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode=mode,
        user_text=last_data["prompt"],
        platform=platform,
        language=lang,
    )

    prompt_engine.set_last_prompt(user_id, prompt=last_data["prompt"], mode=mode, result=result)

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(callback.message, result, reply_markup=get_prompt_actions_keyboard())


@router.callback_query(F.data == "act_translate")
async def callback_translate_last(callback: CallbackQuery) -> None:
    """Oxirgi natijani tarjima qilish."""
    await callback.answer("🌐 Tarjima qilinmoqda...")
    user_id = callback.from_user.id
    last_data = prompt_engine.get_last_prompt(user_id)

    if not last_data or not last_data.get("prompt"):
        await callback.message.answer("⚠️ Oxirgi prompt topilmadi.")
        return

    user_data = prompt_engine.get_user_data(user_id)
    lang = user_data.get("language", "uz")

    wait_msg = await callback.message.answer("⏳ *Professional prompt tarjimasi tayyorlanmoqda...*", parse_mode="Markdown")

    result = await ai_service.generate_prompt(
        mode="translate",
        user_text=last_data["prompt"],
        language=lang,
    )

    try:
        await wait_msg.delete()
    except Exception:
        pass

    await send_smart_message(callback.message, result, reply_markup=get_prompt_actions_keyboard())


@router.callback_query(F.data == "act_change_platform")
async def callback_change_platform(callback: CallbackQuery) -> None:
    """Platformani tezkor almashtirish menyusi."""
    await callback.answer()
    user_id = callback.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    current_platform = user_data.get("platform", "Universal")

    text = f"🎯 Hozirgi platforma: `{current_platform}`\nKerakli platformani tanlang:"
    await callback.message.answer(
        text,
        reply_markup=get_platform_selection_keyboard(current_platform),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "act_main_menu")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Bosh menyuga o'tish."""
    await state.clear()
    await callback.answer()
    user_id = callback.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")

    text = (
        "🚀 **PROMPT MASTER AI**\n\n"
        f"🎯 **Platforma**: `{platform}`\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )
    await callback.message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
