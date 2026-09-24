# 🚀 PROMPT MASTER AI — Telegram Bot

Oddiy, xato yoki noaniq g‘oyalarni professional darajadagi, kuchli, aniq va AI image/video generatorlar (Midjourney, Flux, Kling, Runway, Sora, DALL-E) uchun optimallashtirilgan promptga aylantiruvchi professional Telegram bot.

---

## 🌟 Asosiy Imkoniyatlar

1. 🖼️ **Rasm uchun Prompt**: Foydalanuvchining qisqa g‘oyasini 25 xil parametr (lighting, camera, lens, composition, texture, style) bo‘yicha tahlil qilib, professional promptga aylantiradi.
2. 🎬 **Video uchun Prompt**: Kamera harakati, obyektlar fizikasi, yoritish, uzluksizlik va vaqt segmentlari (0-3s, 3-7s, 7-10s) bilan video prompt yaratadi.
3. 📸 **Image-to-Video**: Rasm yuborilganda personajning yuzi, kiyimi va atrof-muhitini saqlagan holda silliq kinematografik harakat ssenariysi tuzadi.
4. 🛠️ **Promptni Tuzatish**: Kuchsiz yoki xato yozilgan promptni tahlil qilib, kamchiliklarini ko‘rsatadi va mukammal variantga keltiradi.
5. 🚀 **Promptni Kuchaytirish (Creative Boost)**: Mavjud g‘oyani yo‘qotmasdan, unga kinematik chuqurlik va vizual boylik qo‘shadi.
6. 🔄 **Professional Tarjima**: Oddiy so‘zma-so‘z tarjima emas, balki AI generatorlar tushunadigan professional atamalar bilan O‘zbekcha <-> Inglizcha tarjima qiladi.
7. 🎯 **12 xil Platformaga Moslashuv**:
   - Universal
   - Midjourney (v6.1 parametrlar bilan)
   - Flux
   - Gemini
   - ChatGPT (DALL-E)
   - Veo
   - Sora
   - Kling
   - Runway (Gen-3)
   - Hailuo (Minimax)
   - Pika
   - Luma
8. 🌐 **Ikki tilli interfeys**: 🇺🇿 O‘zbekcha va 🇬🇧 English.
9. 📋 **Qulay nusxa olish**: Har bir prompt alohida markdown kod bloki ichida chiqariladi (bir marta bosish bilan copy qilinadi).

---

## 📂 Loyiha Strukturasi

```text
promt bot/
│
├── bot.py                     # Asosiy ishga tushirish fayli
├── config.py                  # Sozlamalar va muhit o'zgaruvchilari
├── requirements.txt           # Kerakli Python kutubxonalari
├── .env                       # API kalitlar (maxfiy)
├── .env.example               # Namuna sozlama fayli
├── .gitignore                 # Git uchun cheklovlar
├── README.md                  # Loyiha hujjatlari
│
├── handlers/                  # Bot buyruqlari va xabarlar ishlovchilari
│   ├── __init__.py
│   ├── start.py               # /start, /help va menyu
│   ├── image.py               # Rasm promptlari
│   ├── video.py               # Video va Image-to-Video
│   ├── prompt.py              # Tuzatish, kuchaytirish va inline amallar
│   ├── translate.py          # Tarjima moduli
│   ├── settings.py           # Platforma va til sozlamalari
│   └── states.py             # FSM holatlari
│
├── services/                  # Biznes mantiq va tashqi servislar
│   ├── __init__.py
│   ├── ai_service.py          # Google Gemini API integratsiyasi
│   └── prompt_engine.py       # Foydalanuvchi ma'lumotlari va keshlash
│
├── keyboards/                 # Telegram klaviaturalari
│   ├── __init__.py
│   └── keyboards.py           # Reply va Inline tugmalar
│
├── prompts/                   # AI Prompt Engine arxitekturasi
│   ├── __init__.py
│   └── system_prompt.py       # PROMPT MASTER AI professional tizim prompti
│
└── utils/                     # Yordamchi vositalar
    ├── __init__.py
    └── helpers.py             # Xabarlarni xavfsiz bo'lish va formatlash
```

---

## ⚙️ O‘rnatish va Ishga Tushirish

### 1. Python talabi
Python 3.10 yoki undan yuqori versiya (tavsiya etiladi: Python 3.11+).

### 2. Kutubxonalarni o‘rnatish
Terminal yoki buyruqlar satrida:
```bash
pip install -r requirements.txt
```

### 3. API kalitlarni sozlash
Loyihadagi `.env` faylini oching va kalitlaringizni kiriting:
```ini
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
GEMINI_API_KEY=AIzaSy...sizning_gemini_api_kalitingiz
GEMINI_MODEL=gemini-2.5-flash
```

* **Telegram Bot Token olish:** Telegramda [@BotFather](https://t.me/BotFather) orqali yangi bot oching va berilgan tokenni oling.
* **Gemini API Key olish:** [Google AI Studio](https://aistudio.google.com/) saytiga kiring va bepul API kalit yarating.

### 4. Botni ishga tushirish
```bash
python bot.py
```

Konsolda quyidagi yozuv paydo bo‘ladi:
```text
Bot muvaffaqiyatli ishga tushdi va xabarlarni qabul qilishga tayyor! 🚀
```

Endi Telegram botingizga kirib `/start` tugmasini bosing!

---

## 🛡️ Xatoliklarni boshqarish
- API kaliti kiritilmagan bo‘lsa, bot o‘chib qolmaydi, foydalanuvchiga tushunarli ogohlantirish beradi.
- Telegram'ning 4096 belgilik cheklovi `utils/helpers.py` orqali avtomatik nazorat qilinadi va xabarlar xavfsiz bo‘linadi.
- Foydalanuvchilarning tanlagan platformasi va tili `user_preferences.json` faylida avtomatik saqlanib boradi.
