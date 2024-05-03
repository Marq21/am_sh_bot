from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from utils import handle_json

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("Начинаю поиск квартир")
    data = handle_json("items.json")
    await msg.answer(data)
