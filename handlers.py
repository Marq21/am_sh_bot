import logging
import time

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import NEWS_CHANNEL
from parser import parse
from utils import handle_json, format_news_category

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message, scheduler: AsyncIOScheduler):
    scheduler.add_job(check, 'interval', minutes=122, kwargs={'msg': msg})


@router.channel_post(Command('check'))
async def check(msg: Message):
    data = await handle_json("items.json")
    for category in data:
        await msg.bot.send_message(NEWS_CHANNEL, f'<b>{category}</b>:\n\n{format_news_category(data[category])}',
                                   )


@router.message(Command('parse'))
async def parse_data(msg: Message):
    start = time.time()
    await parse()
    logging.info(f"Done for {parse_data.__name__} {time.time() - start}ms")
