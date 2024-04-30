from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import kb

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("Выберите категорию для поиска", reply_markup=await kb.get_keyboard_text("https://www.avito.ru/"))
    # data = handle_json("items.json")
    # await msg.answer(data)
