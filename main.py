import math
import requests
from config import user_name, password
from selectolax.parser import HTMLParser
import csv

SITE = 'https://'

def write_csv(data, order):
    with open('products.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)

def get_data(url, session):
    html = session.get(url).text
    tree = HTMLParser(html)
    title = tree.css_first('h1').text()
    descr = tree.css_first('span[itemprop="description"]').text()
    items = tree.css('.catalog-item-offers > tbody > tr > td')
    for item in items:
        try:
            image = item.css_first('.catalog-image > a').attributes['href']
        except:
            image = ''

        try:
            title = item.css_first('.catalog-image > a').attributes[
                'href']
        except:
            title = ''

        try:
            prices = item.css('.catalog-price')
            price_1 = prices[0].text()
            price_2 = prices[-1].text()
        except:
            price_1 = ''
            price_2 = ''

        try:
            descr = item.css_first('.catalog-image > a').attributes[
                'href']
            descr = descr.replace('\n', '').replace('\t', '').strip()
            descr = descr.replace('В корзину', '').replace('цена:', '')
            descr = descr.replace(price_1, '').replace(price_2, '')
        except:
            descr = ''

        data = {
            'url': url,
            'img': image,
            'Наименование товара': title,
            'Описание': descr,
            'Цена 1': price_1,
            'Цена 2': price_2
        }

        order = list(data)

        write_csv(data, order)


def get_links(url, session):
    html = requests.get(url)
    tree = HTMLParser(html.text)
    links = tree.css('.catalog-item-title > a')
    for link in links:
        url = SITE + link.attributes['href']
        get_data(url, session)

def get_pagination(url):
    html = requests.get(url)
    tree = HTMLParser(html.text)
    text = tree.css_first('.text').text()
    text = text.split(' ')[-1]
    count = int(text)/30
    count = math.ceil(count)
    return count


def main():
    url = SITE + '/login/'

    with requests.session() as session:
        session.post(url, auth=(user_name, password))

        url = SITE + '/catalog/?page='

        count = get_pagination(url)
        for i in range(1, count+1):
            page_link = url + '?page=' + str(i)
            get_links(page_link, session)


if __name__ == '__main__':
    main()