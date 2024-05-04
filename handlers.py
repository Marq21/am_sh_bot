from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from utils import handle_json

router = Router()


class UrlState(StatesGroup):
    url = State()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("Начинаю поиск")
    data = handle_json("items.json")
    await msg.answer(data)


@router.message(Command('find'))
async def get_user_url(msg: Message, state: FSMContext):
    await state.set_state(UrlState.url)
    await msg.answer("Отправьте <b>сконфигурированный url-адрес</b>, по которому будет осуществляться поиск")


@router.message(UrlState.url)
async def set_user_url(msg: Message, state: FSMContext):
    await state.update_data(url=msg.text)
    user_url = await state.get_data()
    await msg.answer(f"URL: {user_url['url']}")
    await state.clear()
