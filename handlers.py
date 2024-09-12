import logging
import time

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import NEWS_CHANNEL
from parsers.ria_parser import parse as ria_parse
from parsers.vedomosti_parser import parse as ved_parse
from utils import handle_json, format_news_category, get_emoji_by_category, format_ria_news_messages

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message, scheduler: AsyncIOScheduler):
    scheduler.add_job(check, 'interval', minutes=122, kwargs={'msg': msg})
    scheduler.add_job(check_ria, 'interval', minutes=31, kwargs={'msg': msg})


@router.channel_post(Command('check'))
async def check(msg: Message):
    data = await handle_json("data/items_vedomosti.json")
    for category in data:
        emoji = get_emoji_by_category(category)
        await msg.bot.send_message(NEWS_CHANNEL,
                                   f'{emoji} <b>{category}</b>:\n\n{format_news_category(data[category])}')


@router.message(Command('check_ria'))
async def check_ria(msg: Message):
    data = await handle_json("data/items_ria.json")
    for pub_date in sorted(data):
        await msg.answer(f'💫Риа новости💫:\n\n{format_ria_news_messages(data[pub_date])}')


@router.message(Command('parse_vedomosti'))
async def parse_vedomosti_data(msg: Message):
    start = time.time()
    await ved_parse()
    logging.info(f"Done for {parse_vedomosti_data.__name__} {time.time() - start}ms")


@router.message(Command('parse_ria'))
async def parse_ria_data(msg: Message):
    start = time.time()
    await ria_parse()
    logging.info(f"Done for {parse_ria_data.__name__} {time.time() - start}ms")
