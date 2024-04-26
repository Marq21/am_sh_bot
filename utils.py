import json


def handle_json(json_data):
    with open(json_data, encoding='utf-8') as jd:
        data = json.loads(jd.read())
    return __format_json_for_tg_message(data)


def __format_json_for_tg_message(data: dict) -> str:
    result = str()
    for elem in data[:10]:
        result += f'<a href="{elem['href']}">{elem['name']}</a>\n{elem['price']}\n{elem['description']}\n\n'
    return result
