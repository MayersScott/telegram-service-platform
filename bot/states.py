from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class NewRequest(StatesGroup):
    title = State()
    description = State()
