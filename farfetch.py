from parsers import pars_lib
from bs4 import BeautifulSoup
from unidecode import unidecode


links = ['https://www.farfetch.com/ru/shopping/men/shoes-2/items.aspx?page=',       # Мужские кросовки
         'https://www.farfetch.com/ru/shopping/women/shoes-1/items.aspx?page=']     # Женские кроссовки

# Концы ссылок:
links_ends = ['&view=90&scale=282&category=137174',
              '&view=90&scale=274&category=136310']

positions = []
json = []


def get_positions(url, driver, page=1, n=0):
    global positions
    if page == 1:
        html = BeautifulSoup(pars_lib.get_html(url[0] + str(page) + url[1], driver, 1), 'lxml')
        n = unidecode(html.find('div', {'data-test': 'page-number'}).string)
        i = -1
        while n[i] != ' ':
            i = i - 1
        n = int(n[i:].strip())
    else:
        html = BeautifulSoup(pars_lib.get_html(url[0] + str(page) + url[1], driver, 0.05), 'lxml')

    if page < n:
        positions.extend(html.find_all('li', {'data-test': 'productCard'}))
        page += 1
        return get_positions(url, driver, page, n)
    else:
        positions.extend(html.find_all('li', {'data-test': 'productCard'}))


def type_and_model_splitter(type_model, i=0):
    ord_of_char = ord(type_model[i])
    if ord_of_char < 123 and ord_of_char != 32:
        if i != 0:
            return [type_model[:i-1].strip(), type_model[i:].strip()]
        else:
            return ['', type_model[i:].strip()]
    else:
        i += 1
        if i != len(type_model):
            return type_and_model_splitter(type_model, i)
        else:
            return [type_model[:i].strip(), type_model[i:].strip()]


def get_data():
    global json, positions
    browser = pars_lib.open_browser()
    for i in range(len(links)):
        get_positions([links[i], links_ends[i]], browser)
        json_positions = []
        for j in range(len(positions)):
            json_positions.append({})
            json_positions[j]['table_name'] = 'farfetch'
            json_positions[j]['Vars'] = {}
            if i == 1:
                json_positions[j]['Vars']['sex'] = 'Мужские'
            else:
                json_positions[j]['Vars']['sex'] = 'Женские'
            type_model = type_and_model_splitter(positions[j].find('p').string.strip())
            json_positions[j]['Vars']['type'] = type_model[0]
            json_positions[j]['Vars']['brand'] = positions[j].find('h3', {'itemprop': 'brand'}).string
            json_positions[j]['Vars']['model'] = type_model[1]
            try:
                json_positions[j]['Vars']['no_sale_price'] = \
                    int(unidecode(positions[j].find('span', {'data-test': 'initialPrice'}).string[:-2]).replace(' ', ''))
            except AttributeError:
                json_positions[j]['Vars']['no_sale_price'] = \
                    int(unidecode(positions[j].find('span', {'data-test': 'price'}).string[:-2]).replace(' ', ''))
            finally:
                json_positions[j]['Vars']['price'] = \
                    int(unidecode(positions[j].find('span', {'data-test': 'price'}).string[:-2]).replace(' ', ''))
            json_positions[j]['Vars']['link'] = 'https://www.farfetch.com' + positions[j].find('a')['href']
            json_positions[j]['Vars']['shop'] = 'farfetch'
        json.extend(json_positions)
        positions.clear()
    pars_lib.close_browser(browser)
    return json
