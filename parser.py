import asyncio
import json

import httpx
from bs4 import BeautifulSoup

data = {}


async def main():
    async with httpx.AsyncClient() as client:
        xml_response = await client.get('https://www.vedomosti.ru/rss/news.xml')
        soup = BeautifulSoup(xml_response.text, 'xml')

        items = soup.find_all('item')
        for item in items:
            category = item.find('category').text
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            article_data = {
                'title': title,
                'link': link,
                'pub_date': pub_date,
            }
            if data.get(category):
                data[category].append(article_data)
            else:
                data[category] = [article_data]
    save_data(data)


def save_data(dict_data: dict):
    with open("items.json", "w", encoding='utf-8') as f:
        json.dump(dict_data, f, ensure_ascii=False, indent=4)


def parse():
    main()


if __name__ == '__main__':
    asyncio.run(main())
