from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import (
    get_settings_keyboard,
    get_platform_selection_keyboard,
    get_language_selection_keyboard,
    get_main_menu_keyboard,
)
from services.prompt_engine import prompt_engine

router = Router(name="settings_router")


@router.message(F.text == "⚙️ Sozlamalar")
async def open_settings(message: Message) -> None:
    """Sozlamalar bo'limini ochish."""
    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    text = (
        "⚙️ **BOT SOZLAMALARI**\n\n"
        "O'zingiz ishlatayotgan AI generator platformasini va qulay tilni tanlang.\n"
        "Barcha yangi promptlar aynan siz tanlagan platforma talablariga moslab beriladi."
    )
    await message.answer(
        text,
        reply_markup=get_settings_keyboard(platform, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "set_choose_platform")
async def choose_platform_menu(callback: CallbackQuery) -> None:
    """Platformalar ro'yxatini ko'rsatish."""
    user_id = callback.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    current_platform = user_data.get("platform", "Universal")

    text = (
        "🎯 **AI GENERATOR PLATFORMASINI TANLANG:**\n\n"
        "Promptlar tanlangan platforma sintaksisi va parametrlariga moslashtiriladi:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_platform_selection_keyboard(current_platform),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("sel_plat:"))
async def select_platform_handler(callback: CallbackQuery) -> None:
    """Yangi platformani saqlash."""
    platform = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    prompt_engine.set_platform(user_id, platform)

    user_data = prompt_engine.get_user_data(user_id)
    lang = user_data.get("language", "uz")

    await callback.answer(f"✅ Platforma o'rnatildi: {platform}", show_alert=False)

    text = (
        "⚙️ **BOT SOZLAMALARI**\n\n"
        f"✅ Platforma muvaffaqiyatli saqlandi: **{platform}**\n\n"
        "Endi bot sizga aynan shu platformaga mos promptlar tayyorlaydi."
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_settings_keyboard(platform, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "set_choose_lang")
async def choose_language_menu(callback: CallbackQuery) -> None:
    """Til tanlash menyusini ko'rsatish."""
    user_id = callback.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    current_lang = user_data.get("language", "uz")

    text = "🌐 **INTERFEYS VA JAVOB TILINI TANLANG:**"
    await callback.message.edit_text(
        text,
        reply_markup=get_language_selection_keyboard(current_lang),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("sel_lang:"))
async def select_language_handler(callback: CallbackQuery) -> None:
    """Yangi tilni saqlash."""
    lang_code = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    prompt_engine.set_language(user_id, lang_code)

    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")

    lang_name = "O'zbekcha" if lang_code == "uz" else "English"
    await callback.answer(f"✅ Til o'rnatildi: {lang_name}", show_alert=False)

    text = (
        "⚙️ **BOT SOZLAMALARI**\n\n"
        f"✅ Til muvaffaqiyatli o'zgartirildi: **{lang_name}**"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_settings_keyboard(platform, lang_code),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "set_back_to_settings")
async def back_to_settings_menu(callback: CallbackQuery) -> None:
    """Sozlamalar asosiy menyusiga qaytish."""
    user_id = callback.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")
    lang = user_data.get("language", "uz")

    text = (
        "⚙️ **BOT SOZLAMALARI**\n\n"
        "O'zingiz ishlatayotgan AI generator platformasini va qulay tilni tanlang."
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_settings_keyboard(platform, lang),
        parse_mode="Markdown",
    )
    await callback.answer()
