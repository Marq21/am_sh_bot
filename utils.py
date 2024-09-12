import json
import random
from datetime import datetime

from config import EMOJIS


async def handle_json(json_data):
    with open(json_data, encoding='utf-8') as jd:
        data = json.loads(jd.read())
    return data


def format_date(date_string: str):
    return datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')


def format_news_category(category_items: dict) -> str:
    """formatting vedomosti site"""
    result = str()
    for item in category_items:
        result += (f'{item['title']}\n\nОпубликовано: {item['pub_date']}\n<a href="{item['link']}">Читать '
                   f'полностью</>\n\n')
    return result


def format_ria_news_messages(data: dict) -> str:
    """formatting ria-novosti site"""
    result = (f'{data['title']}\n\nОпубликовано: {data['pub_date']}\n<a href="{data['link']}">Читать '
              f'полностью</>\n\n')
    return result


def get_emoji_by_category(category: str) -> str:
    """
        split category because they have subcategories by space
        split method return two elements [category, subcategory]
    """
    split_category = str.split(category, '/')[0].strip()
    emoji_list = EMOJIS.setdefault(split_category, '')
    emoji = random.choice(emoji_list) if len(emoji_list) > 1 else ''
    return emoji
