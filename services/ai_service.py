import base64
import json
import logging
from typing import Optional, List, Dict, Any
import aiohttp

from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts.system_prompt import (
    BASE_SYSTEM_PROMPT,
    get_image_prompt_instruction,
    get_video_prompt_instruction,
    get_fix_prompt_instruction,
    get_enhance_prompt_instruction,
    get_translate_prompt_instruction,
)

logger = logging.getLogger(__name__)

GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


class AIService:
    """Google Gemini API orqali professional promptlarni yaratish xizmati.
    
    Tashqi og'ir kutubxonalarga bog'lanib qolmaslik va to'liq asinxronlikni
    ta'minlash uchun to'g'ridan-to'g'ri rasmiy Gemini REST API bilan ishlaydi.
    """

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = GEMINI_MODEL or "gemini-3.6-flash"
        self._check_config()

    def _check_config(self) -> bool:
        """API kaliti sozlanganligini tekshirish."""
        if not self.api_key or self.api_key in ("your_gemini_api_key_here", ""):
            logger.warning("GEMINI_API_KEY sozlanmagan. Iltimos .env faylini to'ldiring.")
            return False
        return True

    async def _call_gemini_rest(
        self,
        system_prompt: str,
        user_prompt: str,
        image_bytes: Optional[bytes] = None,
        model_name: Optional[str] = None,
    ) -> str:
        """Gemini REST API orqali so'rov yuborish."""
        current_model = model_name or self.model
        url = f"{GEMINI_API_BASE_URL}/{current_model}:generateContent?key={self.api_key}"

        # Foydalanuvchi qismini shakllantirish
        parts: List[Dict[str, Any]] = []

        if image_bytes:
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": encoded_image,
                }
            })

        parts.append({"text": user_prompt})

        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": parts,
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 2048,
            },
        }

        headers = {"Content-Type": "application/json"}

        timeout = aiohttp.ClientTimeout(total=45)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                status = resp.status
                text_response = await resp.text()

                if status == 200:
                    data = json.loads(text_response)
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts_resp = candidates[0].get("content", {}).get("parts", [])
                        if parts_resp and "text" in parts_resp[0]:
                            return parts_resp[0]["text"].strip()
                    return "❌ Natija bo'sh qaytdi. Boshqa g'oya bilan urinib ko'ring."

                elif status in (400, 403):
                    # Kalit yoki model noto'g'ri bo'lishi mumkin
                    if "API_KEY_INVALID" in text_response or status == 403:
                        logger.error(f"Gemini API kaliti xato: {text_response}")
                        return "⚠️ Gemini API kaliti yaroqsiz yoki ruxsat yo'q. `.env` faylini tekshiring."
                    
                    # Agar model topilmasa, fallback sifatida gemini-1.5-flash ga o'tamiz
                    if current_model != "gemini-1.5-flash":
                        logger.warning(f"{current_model} modelida xatolik ({text_response[:100]}), gemini-1.5-flash bilan urinilmoqda...")
                        return await self._call_gemini_rest(
                            system_prompt, user_prompt, image_bytes, model_name="gemini-1.5-flash"
                        )
                    return f"⚠️ So'rovda xatolik yuz berdi (HTTP {status})."

                elif status == 429:
                    logger.warning("Gemini API so'rov limiti oshdi (Rate limit / Quota exceeded).")
                    return "⚠️ API so'rovlar limiti tugadi (Quota exceeded). Iltimos, 1-2 daqiqadan so'ng qayta urinib ko'ring."

                else:
                    logger.error(f"Gemini API xatosi ({status}): {text_response}")
                    return f"❌ Server xatosi yuz berdi (Status: {status}). Bir ozdan so'ng qayta urinib ko'ring."

    async def generate_prompt(
        self,
        mode: str,
        user_text: str,
        platform: str = "Universal",
        language: str = "uz",
        image_bytes: Optional[bytes] = None,
    ) -> str:
        """Prompt yaratish uchun yagona xizmat funksiyasi."""
        # Yangilangan API keyni tekshirish
        from config import GEMINI_API_KEY, GEMINI_MODEL
        self.api_key = GEMINI_API_KEY
        self.model = GEMINI_MODEL

        if not self._check_config():
            return (
                "⚠️ **Tizim xabari**: Gemini API kaliti sozlanmagan!\n\n"
                "Iltimos, bot o'rnatilgan papkadagi `.env` faylini oching va "
                "`GEMINI_API_KEY` parametrini to'ldiring.\n"
                "Kalitni bu yerdan olish mumkin: https://aistudio.google.com/"
            )

        # Rejimga mos ko'rsatmani tayyorlash
        if mode == "image":
            instruction = get_image_prompt_instruction(user_text, platform, language)
        elif mode == "video":
            instruction = get_video_prompt_instruction(
                user_text, platform, language, has_image=image_bytes is not None
            )
        elif mode == "fix":
            instruction = get_fix_prompt_instruction(user_text, platform, language)
        elif mode == "enhance":
            instruction = get_enhance_prompt_instruction(user_text, platform, language)
        elif mode == "translate":
            instruction = get_translate_prompt_instruction(user_text, language)
        else:
            instruction = get_image_prompt_instruction(user_text, platform, language)

        try:
            return await self._call_gemini_rest(
                system_prompt=BASE_SYSTEM_PROMPT,
                user_prompt=instruction,
                image_bytes=image_bytes,
            )
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Internet aloqasi xatosi: {e}")
            return "🌐 Internet yoki Google serveriga ulanishda xatolik yuz berdi. Tarmoqni tekshiring."
        except TimeoutError:
            logger.error("Gemini API timeout")
            return "⏳ Server javob berish vaqti tugadi (Timeout). Iltimos, qayta urinib ko'ring."
        except Exception as e:
            logger.error(f"Kutilmagan xatolik: {e}", exc_info=True)
            return f"❌ Prompt generatsiyasida xatolik: `{str(e)[:150]}`"


# Global singleton nusxa
ai_service = AIService()
