from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import kb
import text
from utils import handle_json

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    data = handle_json("items.json")
    await msg.answer(data)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def message_handler(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
