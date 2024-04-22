from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import kb
import text

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def message_handler(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
