import json
from datetime import datetime

import validators.url


async def handle_json(json_data):
    with open(json_data, encoding='utf-8') as jd:
        data = json.loads(jd.read())
    return await __format_json_for_tg_message(data)


def format_date(date_string: str):
    return datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')


async def __format_json_for_tg_message(data: dict) -> str:
    result = str()
    for elem in data[:10]:
        result += f'<a href="{elem['href']}">{elem['name']}</a>\n{elem['price']}\n{elem['description']}\n\n'
    return result


async def validate_user_filter_href(href: str) -> bool:
    if "https://www.avito.ru/" not in href:
        return False
    else:
        return validators.url(href)
