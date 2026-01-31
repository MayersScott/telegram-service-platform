from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api_client import APIClient
from states import NewRequest

router = Router()
api = APIClient()

STATUS_LABELS: dict[str, str] = {
    "new": "Новая",
    "in_progress": "В работе",
    "done": "Завершена",
    "cancelled": "Отменена",
}

def status_label(status: str) -> str:
    return STATUS_LABELS.get(status, status)


@router.message(Command("start"))
async def start(message: Message) -> None:
    if message.from_user is None:
        return
    await api.upsert_user(tg_user_id=message.from_user.id, tg_chat_id=message.chat.id)
    await message.answer(
        "Привет! Я бот заявок.\n\n"
        "Команды:\n"
        "/new — создать заявку\n"
        "/my — мои заявки\n"
    )


@router.message(Command("new"))
async def new_request(message: Message, state: FSMContext) -> None:
    await state.set_state(NewRequest.title)
    await message.answer("Ок! Напиши тему заявки (коротко).")


@router.message(NewRequest.title)
async def new_request_title(message: Message, state: FSMContext) -> None:
    title = (message.text or "").strip()
    if not title:
        await message.answer("Тема не должна быть пустой. Попробуй ещё раз.")
        return
    await state.update_data(title=title)
    await state.set_state(NewRequest.description)
    await message.answer("Теперь опиши детали (можно одним сообщением).")


@router.message(NewRequest.description)
async def new_request_description(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    data = await state.get_data()
    title = data.get("title", "Без темы")
    description = (message.text or "").strip() or None

    item = await api.create_request(
        title=title,
        description=description,
        tg_user_id=message.from_user.id,
        tg_chat_id=message.chat.id,
    )
    await state.clear()
    await message.answer(f"Готово ✅\nСоздана заявка #{item['id']} со статусом: {item['status']}\n\n/my — мои заявки")


@router.message(Command("my"))
async def my_requests(message: Message) -> None:
    if message.from_user is None:
        return
    items = await api.list_my_requests(tg_user_id=message.from_user.id)
    if not items:
        await message.answer("У тебя пока нет заявок. /new чтобы создать.")
        return

    lines = ["Ваши заявки:"]
    for it in items[:10]:
        lines.append(f"№{it['id']} | {status_label(it['status'])} | {it['title']}")
    await message.answer("\n".join(lines))

