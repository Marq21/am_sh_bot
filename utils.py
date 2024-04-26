import json


def handle_json(json_data):
    with open(json_data, encoding='utf-8') as jd:
        data = json.loads(jd.read())
    return __format_json_for_tg_message(data)


def __format_json_for_tg_message(data: dict) -> str:
    result = str()
    for elem in data[:10]:
        print(elem['href'])
        result += f'{elem['href']}\n{elem['name']}\n{elem['price']}\n{elem['description']}\n\n'
    print(result)
    return result
