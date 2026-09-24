import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Tokens & Keys
BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest").strip()

# Supported Platforms
SUPPORTED_PLATFORMS = [
    "Universal",
    "Midjourney",
    "Flux",
    "Gemini",
    "ChatGPT",
    "Veo",
    "Sora",
    "Kling",
    "Runway",
    "Hailuo",
    "Pika",
    "Luma",
]

# Supported Languages
SUPPORTED_LANGUAGES = {
    "uz": "🇺🇿 O‘zbekcha",
    "en": "🇬🇧 English",
}

DEFAULT_PLATFORM = "Universal"
DEFAULT_LANGUAGE = "uz"


def validate_config():
    """Ensure mandatory environment variables are provided."""
    missing = []
    if not BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")

    if missing:
        raise ValueError(
            f"❌ Quyidagi muhim konfiguratsiya parametrlar .env faylida topilmadi: {', '.join(missing)}\n"
            f"Iltimos, .env faylini to'ldiring (.env.example ga qarang)."
        )
