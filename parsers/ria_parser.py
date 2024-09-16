import asyncio
import datetime
import json

import httpx
import pytz
from bs4 import BeautifulSoup, ResultSet

from utils import format_date


async def main():
    async with httpx.AsyncClient() as client:
        xml_response = await client.get('https://ria.ru/export/rss2/archive/index.xml')
        soup = BeautifulSoup(xml_response.text, 'xml')
        items = soup.find_all('item')
    data = _parse_to_dict(items)
    save_data(data)


def save_data(dict_data: dict):
    with open("data/items_ria.json", "w", encoding='utf-8') as f:
        json.dump(dict_data, f, ensure_ascii=False, indent=4)


def _parse_to_dict(items: ResultSet) -> dict:
    data = {}
    for item in items:
        pub_date = format_date(item.find('pubDate').text)
        compared_data = datetime.datetime.now(pytz.utc) - datetime.timedelta(minutes=60)
        if pub_date >= compared_data:
            title = item.find('title').text
            link = item.find('link').text
            pub_date = str(pub_date.strftime('%d/%m/%Y %H:%M'))
            article_data = {
                'title': title,
                'link': link,
                'pub_date': pub_date,
            }
            data[pub_date] = article_data

    return data


async def parse():
    await main()


if __name__ == '__main__':
    asyncio.run(main())
