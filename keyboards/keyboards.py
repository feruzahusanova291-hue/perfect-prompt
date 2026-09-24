from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import SUPPORTED_PLATFORMS, SUPPORTED_LANGUAGES


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Bosh menyu reply klaviaturasi."""
    kb = [
        [
            KeyboardButton(text="🖼️ Rasm prompti"),
            KeyboardButton(text="🎬 Video prompti"),
        ],
        [
            KeyboardButton(text="🛠️ Promptni tuzatish"),
            KeyboardButton(text="🚀 Promptni kuchaytirish"),
        ],
        [
            KeyboardButton(text="🔄 Tarjima"),
            KeyboardButton(text="⚙️ Sozlamalar"),
        ],
        [
            KeyboardButton(text="❓ Yordam"),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Amalni bekor qilish yoki orqaga qaytish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Bosh menyu")]],
        resize_keyboard=True,
    )


def get_prompt_actions_keyboard() -> InlineKeyboardMarkup:
    """Natija xabari tagidagi inline amallar tugmalari."""
    buttons = [
        [
            InlineKeyboardButton(text="🚀 Kuchaytirish", callback_data="act_enhance"),
            InlineKeyboardButton(text="🔄 Qayta yaratish", callback_data="act_regenerate"),
        ],
        [
            InlineKeyboardButton(text="🌐 Tarjima qilish", callback_data="act_translate"),
            InlineKeyboardButton(text="🎯 Platformani o'zgartirish", callback_data="act_change_platform"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Bosh menyu", callback_data="act_main_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_settings_keyboard(current_platform: str, current_lang: str) -> InlineKeyboardMarkup:
    """Sozlamalar menyusi (Platforma va Tilni tanlash)."""
    lang_name = SUPPORTED_LANGUAGES.get(current_lang, "O'zbekcha")
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🎯 Platforma: {current_platform}",
                callback_data="set_choose_platform",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🌐 Til: {lang_name}",
                callback_data="set_choose_lang",
            )
        ],
        [
            InlineKeyboardButton(text="⬅️ Bosh menyu", callback_data="act_main_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_platform_selection_keyboard(current_platform: str) -> InlineKeyboardMarkup:
    """Platformalar ro'yxati (har bir qatorda 2 tadan)."""
    rows = []
    current_row = []

    for platform in SUPPORTED_PLATFORMS:
        mark = "✅ " if platform.lower() == current_platform.lower() else ""
        btn = InlineKeyboardButton(
            text=f"{mark}{platform}",
            callback_data=f"sel_plat:{platform}",
        )
        current_row.append(btn)
        if len(current_row) == 2:
            rows.append(current_row)
            current_row = []

    if current_row:
        rows.append(current_row)

    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="set_back_to_settings")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_language_selection_keyboard(current_lang: str) -> InlineKeyboardMarkup:
    """Tilni tanlash inline klaviaturasi."""
    buttons = []
    for code, name in SUPPORTED_LANGUAGES.items():
        mark = "✅ " if code == current_lang else ""
        buttons.append([
            InlineKeyboardButton(
                text=f"{mark}{name}",
                callback_data=f"sel_lang:{code}",
            )
        ])

    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="set_back_to_settings")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
