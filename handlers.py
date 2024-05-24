from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import database.requests as rq
from utils import handle_json, validate_user_filter_href

router = Router()


class UrlState(StatesGroup):
    url = State()


@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("Начинаю поиск")
    data = await handle_json("items.json")
    await msg.answer(data)
    await msg.delete()


@router.message(Command('find'))
async def get_user_url(msg: Message, state: FSMContext):
    await state.set_state(UrlState.url)
    await msg.answer("Отправьте <b>сконфигурированный url-адрес</b>, по которому будет осуществляться поиск")
    await msg.delete()


@router.message(UrlState.url)
async def set_user_url(msg: Message, state: FSMContext):
    await state.update_data(url=msg.text)
    state_data = await state.get_data()
    await msg.answer(f"URL: {state_data['url']}\n {await validate_user_filter_href(state_data['url'])}")
    if await validate_user_filter_href(state_data['url']):
        await rq.set_user(msg.from_user.id, state_data['url'])
        await msg.answer("Успешно сохранил данные в бд")
    else:
        await msg.answer("Ошибка валидации ссылки, введите верную ссылку с сайта www.avito.ru!")
        await msg.answer("Введите или нажмите на комманду '/find', чтобы ввести ссылку заново")
    await state.clear()
