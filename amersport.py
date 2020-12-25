from parsers import pars_lib
from bs4 import BeautifulSoup
from unidecode import unidecode


links = ['https://amersport.ru/brand/converse/style-ox',    # Низкие конверсы
         'https://amersport.ru/brand/converse/style-hi',    # Высокие конверсы
         'https://amersport.ru/brand/drmartens/style-nizkie-botinki/style-vysokie-botinki']     # Мартенсы

json = []
positions = []


def get_positions(link, browser, i=1):
    html = BeautifulSoup(pars_lib.get_html(link + '?p=' + str(i), browser), 'lxml')
    n = html.find('ul', class_='items pages-items').find_all('li')
    if str(n[-1])[11:31] == 'item pages-item-next':
        positions.extend(html.find('ol', class_='products list items product-items').find_all('li'))
        i += 1
        return get_positions(link, browser, i)
    else:
        positions.extend(html.find('ol', class_='products list items product-items').find_all('li'))


def get_data():
    global json
    browser = pars_lib.open_browser()
    for i in range(len(links)):
        get_positions(links[i], browser)
        json_positions = []
        for j in range(len(positions)):
            json_positions.append({})
            json_positions[j]['table_name'] = 'amersport'
            json_positions[j]['Vars'] = {}
            json_positions[j]['Vars']['sex'] = ''
            if i == 0:
                json_positions[j]['Vars']['type'] = 'Низкие кеды'
                json_positions[j]['Vars']['brand'] = 'Converse'
            elif i == 1:
                json_positions[j]['Vars']['type'] = 'Высокие кеды'
                json_positions[j]['Vars']['brand'] = 'Converse'
            else:
                json_positions[j]['Vars']['type'] = 'Ботинки'
                json_positions[j]['Vars']['brand'] = 'Dr. Martens'

            json_positions[j]['Vars']['model'] = positions[j].find('a', class_='product-item-link').string
            if len(positions[j].find_all('span', class_='price')) > 1:
                json_positions[j]['Vars']['no_sale_price'] = int(
                    unidecode(positions[j].find_all('span', class_='price')[0].string[0:-2]).replace(' ', ''))
                json_positions[j]['Vars']['price'] = int(
                    unidecode(positions[j].find_all('span', class_='price')[1].string[0:-2]).replace(' ', ''))
            else:
                json_positions[j]['Vars']['no_sale_price'] = int(
                    unidecode(positions[j].find_all('span', class_='price')[0].string[0:-2]).replace(' ', ''))
                json_positions[j]['Vars']['price'] = int(
                    unidecode(positions[j].find_all('span', class_='price')[0].string[0:-2]).replace(' ', ''))
            json_positions[j]['Vars']['link'] = str(positions[j].find('a')['href'])
            json_positions[j]['Vars']['shop'] = 'amersport'
        json.extend(json_positions)
        positions.clear()
    pars_lib.close_browser(browser)
    return json
