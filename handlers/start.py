import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import get_main_menu_keyboard
from services.prompt_engine import prompt_engine

logger = logging.getLogger(__name__)
router = Router(name="start_router")


@router.message(CommandStart())
@router.message(F.text == "⬅️ Bosh menyu")
@router.message(Command("cancel"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """/start komandasi yoki bosh menyuga qaytish."""
    logger.info(f"Yangi start/menyu buyrug'i qabul qilindi: ID={message.from_user.id} (@{message.from_user.username})")
    await state.clear()
    user_id = message.from_user.id
    user_data = prompt_engine.get_user_data(user_id)
    platform = user_data.get("platform", "Universal")

    text = (
        "🚀 **PROMPT MASTER AI**\n\n"
        "“*Oddiy g‘oyangizni professional AI promptga aylantiring.*”\n\n"
        f"🎯 **Hozirgi platforma**: `{platform}`\n\n"
        "Quyidagi tugmalardan birini tanlang va g‘oyangizni yuboring:"
    )
    await message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")


@router.message(Command("help"))
@router.message(F.text == "❓ Yordam")
async def command_help_handler(message: Message) -> None:
    """Yordam va qo'llanma bo'limi."""
    help_text = (
        "📖 **PROMPT MASTER AI — QO'LLANMA**\n\n"
        "Bu bot sizning oddiy yoki xomaki g'oyalaringizni AI generatorlar "
        "(Midjourney, Flux, Kling, Runway, Sora, DALL-E) uchun mukammal promptga aylantiradi.\n\n"
        "🔹 **Asosiy funksiyalar**:\n"
        "• 🖼️ **Rasm prompti** — G'oyadan cinematic va photorealistic rasm prompti yaratadi.\n"
        "• 🎬 **Video prompti** — Kamera harakati, harakat fizikasi va vaqt segmentlari bilan video prompt tayyorlaydi. Rasm yuborsangiz, Image-to-Video rejimida ishlaydi!\n"
        "• 🛠️ **Promptni tuzatish** — Mavjud promptni tahlil qilib, xatolarini to'g'irlaydi.\n"
        "• 🚀 **Promptni kuchaytirish** — Promptni maksimal darajada boyitadi va kuchaytiradi.\n"
        "• 🔄 **Tarjima** — Oddiy tarjima emas, AI tushunadigan professional atamalar bilan tarjima qiladi.\n"
        "• ⚙️ **Sozlamalar** — Platforma (Midjourney, Flux, Kling...) va tilni sozlash.\n\n"
        "💡 *Maslahat: Chiqqan prompt ustiga bosib bir martada nusxa (copy) olishingiz mumkin!*"
    )
    await message.answer(help_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
