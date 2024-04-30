import json

import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

data_list = []


def main():
    driver = uc.Chrome(headless=True, use_subprocess=False)
    driver.get(
        "https://www.avito.ru/rostov-na-donu/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&context"
        "=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA&f=ASgBAgICAkSSA8YQjt4OAg&s=1")
    elements = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')

    for elem in elements:
        try:
            name = elem.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
            href = elem.find_element(By.CSS_SELECTOR, '[itemprop="url"]').get_attribute("href")
            description = elem.find_element(By.CSS_SELECTOR, '[class*="iva-item-descriptionStep"]').text[:50] + "..."
            price = elem.find_element(By.CSS_SELECTOR, '[data-marker="item-price"]').text
            data = {
                "name": name,
                "href": href,
                "description": description,
                "price": price,
            }
            data_list.append(data)
        except NoSuchElementException as nse:
            print("Элемент отсутствует", nse.msg)
    save_data(data_list)
    driver.close()


def save_data(data: list):
    with open("items.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def parse():
    main()


def get_category_text(url: str):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options, use_subprocess=False)
    driver.implicitly_wait(10)
    driver.get(url)
    elements = driver.find_elements(By.CSS_SELECTOR, '[data-marker*="visual-rubricator/block-"]')
    save_category_data(elements)
    list_text_elements = [element.text for element in elements]
    driver.close()
    return list_text_elements


def save_category_data(category_list):
    for element in category_list:
        name = element.text
        href = element.get_attribute('href')
        data = {
            "name": name,
            "href": href,
        }
        if name:
            data_list.append(data)
    save_data(data_list)


if __name__ == '__main__':
    main()
