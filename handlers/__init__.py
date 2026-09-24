from aiogram import Dispatcher
from handlers.start import router as start_router
from handlers.image import router as image_router
from handlers.video import router as video_router
from handlers.prompt import router as prompt_router
from handlers.translate import router as translate_router
from handlers.settings import router as settings_router


def register_all_handlers(dp: Dispatcher) -> None:
    """Barcha routerlarni dispatcherga ro'yxatdan o'tkazish."""
    dp.include_router(start_router)
    dp.include_router(image_router)
    dp.include_router(video_router)
    dp.include_router(prompt_router)
    dp.include_router(translate_router)
    dp.include_router(settings_router)
