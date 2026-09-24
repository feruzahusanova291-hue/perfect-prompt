from aiogram.fsm.state import State, StatesGroup


class PromptStates(StatesGroup):
    """Prompt bot holatlari (FSM)."""

    waiting_for_image_idea = State()
    waiting_for_video_idea = State()
    waiting_for_fix_prompt = State()
    waiting_for_enhance_prompt = State()
    waiting_for_translate_text = State()
