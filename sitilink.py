from bs4 import BeautifulSoup
import csv
import urllib.request
import re

Base_URL = "https://www.citilink.ru/catalog/mobile/smartfony/-smartfony-na-androide/"


def clear(string):
    string = re.sub(r'\s+', ' ', string)
    clear_string = re.sub(r'\n', '', string)
    return clear_string


def get_html(url):
    response = urllib.request.urlopen(url)
    return response


def get_page_count(html):
    soup = BeautifulSoup(html)
    paggination = soup.find('div', class_='page_listing')
    return int(paggination.find("section").find("ul").find('li', class_='last').a.text)


def pars(html):
    soup = BeautifulSoup(html)
    div = soup.find('div', class_='product_category_list')
    div = div.find('div', class_='block_data__gtm-js block_data__pageevents-js listing_block_data__pageevents-js')
    projects = []
    for block in div.find_all('div', class_='js--subcategory-product-item subcategory-product-item product_data__gtm-js\
     product_data__pageevents-js ddl_product'):
        name = block.find('div', class_='subcategory-product-item__body')
        result_name = re.sub(r'\s+', ' ', name.find('span', class_='h3').a.text)
        result_features = clear(name.p.text)
        price = block.find('div', class_='subcategory-product-item__footer')
        price = price.find('div', class_='subcategory-product-item__price-container')
        price = price.find('span', class_='subcategory-product-item__prices')
        old_price = price.find('span', class_='subcategory-product-item__price subcategory-product-item__price_old')
        normal_price = price.find('span', class_='subcategory-product-item__price subcategory-product-item__price_\
        standart')
        normal_price = normal_price.text
        normal_price = clear(normal_price)
        if not old_price is None:
            old_price = old_price.text
            old_price = clear(old_price)
            projects.append({
                'title': result_name,
                'feature': result_features,
                'price': normal_price,
                'old_price': old_price
            })
        else:
            projects.append({
                'title': result_name,
                'feature': result_features,
                'price': normal_price,
                'old_price': '-'
            })
    return projects


def save(projects, path):
    with open(path, 'w', encoding="utf-8") as csvfile:
        writen = csv.writer(csvfile)
        writen.writerow(('Название', "Характеристики", "Цена", 'Страрая цена'))

        for project in projects:
            writen.writerow((project['title'], project['feature'], project['price'], project['old_price']))


def main():
    page_count = get_page_count(get_html(Base_URL))

    print('Всего найдено страниц %d' % page_count)

    projects = []

    for page in range(1, page_count):
        print('Парсинг %d%%' % (page / page_count * 100))
        projects.extend(pars(get_html(Base_URL + '?available=1&status=55395790&p=%d' % page)))

    save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
