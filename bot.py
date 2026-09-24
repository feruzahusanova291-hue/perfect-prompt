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
import aiohttp
from aiohttp import web

from config import BOT_TOKEN, validate_config
from handlers import register_all_handlers

from collections import deque
import json

log_buffer = deque(maxlen=100)

class BufferLogHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            log_buffer.append(msg)
        except Exception:
            pass

buffer_handler = BufferLogHandler()
buffer_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), buffer_handler],
)
logger = logging.getLogger("PROMPT_MASTER_AI")

BOT_VERSION = "v1.3-debug"


async def start_health_server():
    """Render yoki bulutli xizmatlar uchun HTTP health check serveri."""
    port = int(os.getenv("PORT", 10000))
    app = web.Application()

    async def handle_ping(request):
        return web.Response(
            text=f"PROMPT MASTER AI Bot is healthy and running! 🚀 (Version: {BOT_VERSION})",
            status=200
        )

    async def handle_debug(request):
        data = {
            "version": BOT_VERSION,
            "status": "online",
            "logs": list(log_buffer)[-50:],
        }
        return web.Response(text=json.dumps(data, indent=2), content_type="application/json")

    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    app.router.add_get("/debug", handle_debug)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Render Health Check server ishga tushdi (Port: {port}, Version: {BOT_VERSION})")
    return runner


async def keep_alive():
    """Render bepul tarifida 15 daqiqadan so'ng uxlab qolmasligi uchun self-ping vazifasi."""
    render_url = os.getenv("RENDER_EXTERNAL_URL") or "https://perfect-prompt.onrender.com"
    logger.info(f"Self-ping vazifasi faollashtirildi: {render_url}")
    await asyncio.sleep(60)
    while True:
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{render_url}/health") as resp:
                    logger.info(f"Self-ping muvaffaqiyatli: HTTP {resp.status}")
        except Exception as e:
            logger.debug(f"Self-ping xatosi: {e}")
        await asyncio.sleep(600)  # Har 10 daqiqada bir marta ping


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

    # Webhookni tozalash (foydalanuvchi yuborgan xabarlarni o'chirib yubormaslik)
    await bot.delete_webhook(drop_pending_updates=False)

    # Render yoki bulutli server uchun health check
    health_runner = None
    if "PORT" in os.environ:
        health_runner = await start_health_server()

    # Render sleep rejimiga o'tmasligi uchun self-ping vazifasi
    ping_task = None
    if "PORT" in os.environ or os.getenv("RENDER_EXTERNAL_URL"):
        ping_task = asyncio.create_task(keep_alive())

    logger.info(f"Bot muvaffaqiyatli ishga tushdi va xabarlarni qabul qilishga tayyor! 🚀 ({BOT_VERSION})")

    try:
        while True:
            try:
                logger.info("Polling boshlanmoqda...")
                await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
                logger.warning("Polling to'xtadi. 3 soniyada qayta ishga tushiriladi...")
            except Exception as e:
                logger.error(f"Polling xatosi: {e}. 3 soniyadan so'ng qayta ulaniladi...")
            await asyncio.sleep(3)
    finally:
        if ping_task:
            ping_task.cancel()
        if health_runner:
            await health_runner.cleanup()
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
