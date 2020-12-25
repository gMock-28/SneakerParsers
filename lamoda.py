import time
from parsers import pars_lib
from bs4 import BeautifulSoup


links = ['https://www.lamoda.ru/c/151/shoes-muzhskie-botinki/?page=',           # Мужские ботинки
         'https://www.lamoda.ru/c/2981/shoes-krossovk-kedy-muzhskie/?page=',    # Мужские кеды/кроссовки
         'https://www.lamoda.ru/c/2968/shoes-krossovki-kedy/?page=',            # Женские кеды/кроссовки
         'https://www.lamoda.ru/c/23/shoes-botinki/?page=']                     # Женские ботинки

json = []
positions = []


def get_positions(urls, driver, page=1, n=0):
    global positions
    html = BeautifulSoup(pars_lib.get_html(urls + str(page), driver), 'lxml')
    if page == 1:
        n = int(html.find('span', class_='products-catalog__head-counter').string[:-7])/60 + 1
    if html.find('div', class_='logo-line-wrapper width-wrapper') is not None:
        if page < n:
            positions.extend(html.find_all('div', class_='products-list-item'))
            page += 1
            return get_positions(urls, driver, page, n)
        else:
            positions.extend(html.find_all('div', class_='products-list-item'))
    else:
        get_positions(urls, driver, page, n)


def type_and_model_splitter(type_model, i=0):
    ord_of_char = ord(type_model[i])
    if ord_of_char < 123 and ord_of_char != 32:
        return [type_model[:i-1].strip(), type_model[i:].strip()]
    else:
        i += 1
        if i != len(type_model):
            return type_and_model_splitter(type_model, i)
        else:
            return [type_model[:i-1].strip(), type_model[i:].strip()]


def get_data():
    global json
    browser = pars_lib.open_browser()
    for i in range(len(links)):
        get_positions(links[i], browser)
        json_positions = []
        for j in range(len(positions)):
            json_positions.append({})
            json_positions[j]['table_name'] = 'lamoda'
            json_positions[j]['Vars'] = {}
            if i < 2:
                json_positions[j]['Vars']['sex'] = 'Мужские'
            else:
                json_positions[j]['Vars']['sex'] = 'Женские'
            type_model = positions[j].find('span', class_='products-list-item__type').string.strip()

            if len(type_model) <= 9:
                json_positions[j]['Vars']['type'] = type_model
                json_positions[j]['Vars']['brand'] = str(positions[j].find('div',
                                                                           class_='products-list-item__brand')).split('<s')[0].split('nd">')[-1].strip()
                json_positions[j]['Vars']['model'] = ''
            else:
                type_model = type_and_model_splitter(type_model)
                json_positions[j]['Vars']['type'] = type_model[0]
                json_positions[j]['Vars']['brand'] = str(positions[j].find('div',
                                                                           class_='products-list-item__brand')).split('<s')[0].split('nd">')[-1].strip()
                json_positions[j]['Vars']['model'] = type_model[1]

            try:
                json_positions[j]['Vars']['no_sale_price'] = \
                    int(positions[j].find('span', class_='price__actual').string.replace(' ', ''))
            except AttributeError:
                json_positions[j]['Vars']['no_sale_price'] = \
                    int(positions[j].find('span', class_='price__old').string.replace(' ', ''))

            if positions[j].find('span', class_='price__action') is not None:
                json_positions[j]['Vars']['price'] = \
                    int(positions[j].find('span', class_='price__action').string.replace(' ', ''))
            else:
                json_positions[j]['Vars']['price'] = \
                    int(positions[j].find('span', class_='price__actual').string.replace(' ', ''))

            json_positions[j]['Vars']['link'] = 'https://www.lamoda.ru' + positions[j].find('a')['href']
            json_positions[j]['Vars']['shop'] = 'lamoda'
        time.sleep(10)
        json.extend(json_positions)
        positions.clear()
    pars_lib.close_browser(browser)
    return json


"""
try:
    get_data(links)
finally:
    print(json)
    print(len(json))

browser = pars_lib.open_browser()
html = BeautifulSoup(pars_lib.get_html(links[1], browser), 'lxml')
print(len(html.find_all('div', class_='products-list-item')))
print(html.find_all('div', class_='products-list-item')[-1])
# print(str(html.find('div', class_='products-list-item__brand')).split('<span')[0].split('brand">')[-1].strip())
pars_lib.close_browser(browser)
"""
