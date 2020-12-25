from parsers import pars_lib
from bs4 import BeautifulSoup
from unidecode import unidecode


links = ['https://street-beat.ru/cat/man/obuv/?page=',
         'https://street-beat.ru/cat/woman/obuv/?page=']

brands = ['Nike', 'Jordan', 'adidas Originals', 'Puma', 'Reebok Classic',
          'The North Face', 'New Balance', 'Asics', 'Tommy Jeans', 'Converse',
          'Vans', 'Helly Hansen', 'Fila', 'adidas Performance', 'UGG', 'Timberland',
          'Havaianas', 'Native', 'Under Armour', 'Saucony', 'Dr. Martens']

positions = []
json = []


def get_positions(link, browser, page=1):
    html = BeautifulSoup(pars_lib.get_html(link + str(page), browser, 3), 'lxml')
    print(html)
    if html.find('button', class_='catalog-pagination__next') is None:
        positions.extend(html.find_all('div', class_='view-type_'))
    else:
        positions.extend(html.find_all('div', class_='view-type_'))
        page += 1
        return get_positions(link, browser, page)


def type_and_other_splitter(type_model, i=0):
    ord_of_char = ord(type_model[i])
    if ord_of_char < 123 and ord_of_char != 32:
        return [type_model[:i-1], type_model[i:]]
    else:
        i += 1
        return type_and_other_splitter(type_model, i)


def get_data():
    browser = pars_lib.open_browser()
    for i in range(len(links)):
        get_positions(links[i], browser)
        json_positions = []
        del positions[-1]
        for j in range(len(positions)):
            json_positions.append({})
            json_positions[j]['table_name'] = 'street_beat'
            json_positions[j]['Vars'] = {}
            string = positions[j].find('span', class_='catalog-item__brand').string
            if i == 0:
                json_positions[j]['Vars']['sex'] = 'Мужские'
                if string.find('ужск') != -1:
                    string = string.replace('Мужские', '')
            else:
                json_positions[j]['Vars']['sex'] = 'Женские'
                if string.find('енск') != -1:
                    string = string.replace('Женские', '')
            type_and_other = type_and_other_splitter(string.strip())
            json_positions[j]['Vars']['type'] = type_and_other[0]
            json_positions[j]['Vars']['brand'] = ''
            for elem in brands:
                if type_and_other[1].find(elem) != -1:
                    json_positions[j]['Vars']['brand'] = elem
                    type_and_other[1] = type_and_other[1].replace(elem, '').strip()
            json_positions[j]['Vars']['model'] = type_and_other[1]
            price_block = positions[j].find('div', class_='price')
            if price_block.find('div', class_='price--old') is not None:
                json_positions[j]['Vars']['no_sale_price'] = int(
                    unidecode(price_block.find('div', class_='price--old').string).replace(' ', ''))
                json_positions[j]['Vars']['price'] = int(
                    unidecode(price_block.find('div', class_='price--current').string).replace(' ', ''))
            else:
                json_positions[j]['Vars']['no_sale_price'] = int(
                    unidecode(price_block.find('div', class_='price--current').string).replace(' ', ''))
                json_positions[j]['Vars']['price'] = int(
                    unidecode(price_block.find('div', class_='price--current').string).replace(' ', ''))
            json_positions[j]['Vars']['link'] = 'https://street-beat.ru' + str(positions[j].find('a')['href'])
            json_positions[j]['Vars']['shop'] = 'street_beat'
        json.extend(json_positions)
        positions.clear()
    pars_lib.close_browser(browser)
    return json
