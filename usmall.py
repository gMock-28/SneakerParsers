from parsers import pars_lib
from bs4 import BeautifulSoup
from unidecode import unidecode


links = ['https://usmall.ru/products/men/shoes/lifestyle-sneakers?page=',
         'https://usmall.ru/products/women/shoes/lifestyle-sneakers?page=']

positions = []
json = []


def get_positions(link, page=1):
    global positions, json
    print(page)
    html = BeautifulSoup(pars_lib.get_html(link + str(page)), 'lxml')
    if html.find('div', class_='c-main-layout') is not None:
        if html.find('a', class_='__next') is not None:
            positions.extend(html.find_all('div', class_='item c-product-item small-only-50 medium-33 xlarge-25'))
            page += 1
            get_positions(link, page)
        else:
            positions.extend(html.find_all('div', class_='item c-product-item small-only-50 medium-33 xlarge-25'))
    else:
        get_positions(link, page)


def get_data():
    global json, positions
    for i in range(len(links)):
        get_positions(links[i])
        json_positions = []
        for j in range(len(positions)):
            json_positions.append({})
            json_positions[j]['table_name'] = 'usmall'
            json_positions[j]['Vars'] = {}
            if i == 0:
                json_positions[j]['Vars']['sex'] = 'Мужские'
            else:
                json_positions[j]['Vars']['sex'] = 'Женские'
            json_positions[j]['Vars']['type'] = 'кроссовки'
            json_positions[j]['Vars']['brand'] = unidecode(positions[j].find('span', class_='__brand').string)
            model = positions[j].find('span', class_='__name').string
            model.replace("Men's", '')
            model.replace("Women's", '')
            json_positions[j]['Vars']['model'] = model
            if positions[j].find('span', class_='__price-value') is None:
                json_positions[j]['Vars']['no_sale_price'] = \
                    int(positions[j].find('span', class_='__price').string[:-3].replace(' ', ''))
                json_positions[j]['Vars']['price'] = \
                    int(positions[j].find('span', class_='__price').string[:-3].replace(' ', ''))
            else:
                json_positions[j]['Vars']['no_sale_price'] = \
                    int(positions[j].find('span', class_='__price-full').string[:-3].replace(' ', ''))
                json_positions[j]['Vars']['price'] = \
                    int(positions[j].find('span', class_='__price-value').string[:-3].replace(' ', ''))
            json_positions[j]['Vars']['link'] = 'https://usmall.ru' + positions[j].find('a')['href']
            json_positions[j]['Vars']['shop'] = 'usmall'
        json.extend(json_positions)
        positions.clear()
    return json


"""
browser = pars_lib.open_browser()
html = BeautifulSoup(pars_lib.get_html(links[0], browser), 'lxml')
print(html.find('div', class_='item c-product-item small-only-50 medium-33 xlarge-25').find('img')['src'])
"""
