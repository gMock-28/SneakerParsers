from parsers import pars_lib
from bs4 import BeautifulSoup
from unidecode import unidecode


link = 'https://www.adidas.ru/obuv?start='
json = []


def type_and_model_splitter(type_model, i=0):
    ord_of_char = ord(type_model[i])
    if ord_of_char < 123 and ord_of_char != 32:
        return [type_model[:i-1], type_model[i:]]
    else:
        i += 1
        return type_and_model_splitter(type_model, i)


def get_data():
    browser = pars_lib.open_browser()

    n = BeautifulSoup(pars_lib.get_html(link, browser), 'lxml')
    n = int(str(n.find_all('span', class_='gl-body gl-body--s gl-no-margin-bottom')[1]).split('<')[-2].split('>')[-1])
    positions = []
    for i in range(n):
        html = BeautifulSoup(pars_lib.get_html(link + str(i * 48), browser, 1.5), 'lxml')
        # print(i+1, ' of ', n, ' pages done')
        positions.extend(html.find_all('div', class_='grid-item___3rAkS'))
    for i in range(len(positions)):
        json.append({})
        json[i]['table_name'] = 'adidas'
        json[i]['Vars'] = {}
        sex_info = str(positions[i].find('div', class_='gl-product-card__category'))
        try:
            sex_info.index('Мужчины')
            json[i]['Vars']['sex'] = 'Мужские'
        except ValueError:
            try:
                sex_info.index('Женщины')
                json[i]['Vars']['sex'] = 'Женские'
            except ValueError:
                json[i]['Vars']['sex'] = ''

        type_model = type_and_model_splitter(positions[i].find('span', class_='gl-product-card__name').string)
        print(i//48, type_model)
        json[i]['Vars']['type'] = type_model[0]
        json[i]['Vars']['brand'] = 'adidas'
        json[i]['Vars']['model'] = type_model[1]
        json[i]['Vars']['no_sale_price'] = 0
        json[i]['Vars']['price'] = int(unidecode(positions[i].find('div', class_='gl-price-item').string)
                                       [:-2].replace(' ', '')
                                       )
        json[i]['Vars']['link'] = 'https://www.adidas.ru/' + str(positions[i].find('a')['href'])
        json[i]['Vars']['shop'] = 'adidas'

    pars_lib.close_browser(browser)
    return json


"""
start = datetime.now()
json_data = get_data(link_adidas)
print('Parsing time: ', datetime.now() - start)
start = datetime.now()
db_lib.insert_elem(json_data)
print('Inserting time: ', datetime.now() - start)
"""
