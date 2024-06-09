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
    result += f'{data["Политика / Международные новости"]}\n'

    return result


async def validate_user_filter_href(href: str) -> bool:
    if "https://www.avito.ru/" not in href:
        return False
    else:
        return validators.url(href)


