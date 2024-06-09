import time

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from parser import parse
from utils import handle_json

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(
        """Чтобы начать введите команду /find\nЧтобы проверить последнюю актуальную выдачу введите команду /check""")
    await msg.delete()


@router.message(Command('check'))
async def get_user_url(msg: Message):
    data = await handle_json("items.json")
    await msg.answer(data)


@router.message(Command('parse'))
async def parse_data(msg: Message):
    await msg.answer("Start parsing")
    start = time.time()
    await parse()
    await msg.answer("Stop parsing")
    print(time.time() - start)
