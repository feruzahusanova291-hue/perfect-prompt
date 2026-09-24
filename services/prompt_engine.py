import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from config import DEFAULT_PLATFORM, DEFAULT_LANGUAGE, BASE_DIR

logger = logging.getLogger(__name__)

DATA_FILE = BASE_DIR / "user_preferences.json"


class PromptEngineService:
    """Foydalanuvchi sozlamalari va oxirgi prompt holatini boshqarish xizmati."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._load_data()

    def _load_data(self):
        """Saqlangan ma'lumotlarni fayldan yuklash."""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception as e:
                logger.error(f"Foydalanuvchi ma'lumotlarini yuklashda xatolik: {e}")
                self._cache = {}
        else:
            self._cache = {}

    def _save_data(self):
        """Ma'lumotlarni faylga saqlash."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Foydalanuvchi ma'lumotlarini saqlashda xatolik: {e}")

    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Foydalanuvchi ma'lumotlarini olish."""
        uid = str(user_id)
        if uid not in self._cache:
            self._cache[uid] = {
                "platform": DEFAULT_PLATFORM,
                "language": DEFAULT_LANGUAGE,
                "last_prompt": "",
                "last_mode": "image",
                "last_result": "",
            }
            self._save_data()
        return self._cache[uid]

    def set_platform(self, user_id: int, platform: str) -> None:
        """Foydalanuvchi tanlagan platformani o'rnatish."""
        data = self.get_user_data(user_id)
        data["platform"] = platform
        self._save_data()

    def set_language(self, user_id: int, language: str) -> None:
        """Foydalanuvchi tanlagan tilni o'rnatish."""
        data = self.get_user_data(user_id)
        data["language"] = language
        self._save_data()

    def set_last_prompt(self, user_id: int, prompt: str, mode: str, result: str = "") -> None:
        """Oxirgi prompt va rejimni saqlash."""
        data = self.get_user_data(user_id)
        data["last_prompt"] = prompt
        data["last_mode"] = mode
        data["last_result"] = result
        self._save_data()

    def get_last_prompt(self, user_id: int) -> Optional[Dict[str, str]]:
        """Oxirgi prompt ma'lumotlarini olish."""
        data = self.get_user_data(user_id)
        if data.get("last_prompt"):
            return {
                "prompt": data["last_prompt"],
                "mode": data.get("last_mode", "image"),
                "result": data.get("last_result", ""),
            }
        return None


# Global singleton nusxa
prompt_engine = PromptEngineService()
