import sys
import asyncio
import logging

# Windows cp1251 konsoli uchun UTF-8 kodirovkasini yoqish
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import os
from aiohttp import web

from config import BOT_TOKEN, validate_config
from handlers import register_all_handlers

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("PROMPT_MASTER_AI")


async def start_health_server():
    """Render yoki bulutli xizmatlar uchun HTTP health check serveri."""
    port = int(os.getenv("PORT", 10000))
    app = web.Application()

    async def handle_ping(request):
        return web.Response(text="PROMPT MASTER AI Bot is healthy and running! 🚀", status=200)

    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Render Health Check server ishga tushdi (Port: {port})")
    return runner


async def set_default_commands(bot: Bot) -> None:
    """Bot uchun standart buyruqlar menyusini o'rnatish."""
    commands = [
        BotCommand(command="start", description="🚀 Botni ishga tushirish"),
        BotCommand(command="help", description="📖 Qo'llanma va yordam"),
        BotCommand(command="cancel", description="❌ Amalni bekor qilish"),
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        logger.warning(f"Buyruqlarni o'rnatishda xatolik: {e}")


async def main() -> None:
    """Asosiy ishga tushirish funksiyasi."""
    logger.info("PROMPT MASTER AI bot ishga tushirilmoqda...")

    # Muhim kalitlarni tekshirish
    try:
        validate_config()
    except ValueError as e:
        logger.error(str(e))
        print("\n" + "=" * 60)
        print(f"XATOLIK: {e}")
        print("Iltimos, .env faylini to'ldiring va botni qayta ishga tushiring.")
        print("=" * 60 + "\n")
        return

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Barcha handlerlarni ulash
    register_all_handlers(dp)

    # Buyruqlar menyusini o'rnatish
    await set_default_commands(bot)

    # Eski kutilmagan yangilanishlarni tozalash (drop pending updates)
    await bot.delete_webhook(drop_pending_updates=True)

    # Render yoki bulutli server uchun health check
    health_runner = None
    if "PORT" in os.environ:
        health_runner = await start_health_server()

    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni qabul qilishga tayyor! 🚀")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        if health_runner:
            await health_runner.cleanup()
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
