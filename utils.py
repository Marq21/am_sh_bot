import json
from datetime import datetime


async def handle_json(json_data):
    with open(json_data, encoding='utf-8') as jd:
        data = json.loads(jd.read())
    return data


def format_date(date_string: str):
    return datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')


def format_news_category(category_items: dict) -> str:
    result = str()
    for item in category_items:
        result += f'{item["title"]}\n<a href="{item["link"]}">Читать полностью</>\nОпубликовано: {item["pub_date"]}\n\n'
    return result
