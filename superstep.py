from parsers import pars_lib
from bs4 import BeautifulSoup
from unidecode import unidecode


link = 'https://superstep.ru/obuv/?PAGEN_1='
json = []


def get_data():
    n = BeautifulSoup(pars_lib.get_html(link), 'lxml').find('div', class_='for-counter').string
    n = int(n[8:13])
    if n//36 != 0:
        n = n // 36 + 1
    else:
        n = n / 36
    positions = []
    i = 1
    while i < n+1:
        positions.extend(BeautifulSoup(pars_lib.get_html(link + str(i)), 'lxml').find_all('div', class_='col-sm-4 col-xs-6'))
        i += 1

    for i in range(len(positions)):
        json.append({})
        json[i]['table_name'] = 'superstep'
        json[i]['Vars'] = {}
        name = str(positions[i].find('p', class_='product-name').find('a')).split('<br/>')[0].split('\t')[-1]
        try:
            name.index('ужск')
            json[i]['Vars']['sex'] = 'Мужские'
            name = name[8:]
        except ValueError:
            try:
                name.index('енск')
                json[i]['Vars']['sex'] = 'Женские'
                name = name[8:]
            except ValueError:
                json[i]['Vars']['sex'] = ''
        ind = name.find(' ')
        json[i]['Vars']['type'] = name[0:ind]
        json[i]['Vars']['brand'] = name[ind:]
        json[i]['Vars']['model'] = unidecode(str(positions[i].find('p', class_='product-name').find('a')['title']))
        price = positions[i].find('p', class_='product-double-price').find_all('span')
        if len(price) == 1:
            json[i]['Vars']['no_sale_price'] = ''
            json[i]['Vars']['price'] = price[0].string[0:-5].replace(' ', '')
        else:
            json[i]['Vars']['no_sale_price'] = price[0].string[0:-5].replace(' ', '')
            json[i]['Vars']['price'] = price[1].string[0:-5].replace(' ', '')
        json[i]['Vars']['link'] = 'https://superstep.ru' + str(positions[i].find('div', class_='product-image-wrapper').find('a')['href'])
        json[i]['Vars']['shop'] = 'superstep'
    return json


"""
start = datetime.now()
data = get_data(link)
print('Parsing time: ', datetime.now() - start)
start = datetime.now()
db_lib.insert_elem(data)
print('Inserting time: ',  datetime.now() - start)
"""
