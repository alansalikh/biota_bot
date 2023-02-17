from bs4 import BeautifulSoup
import requests 
from config import HEADERS, URL, DOMEN
from products import insert_product

# id | name | description | price | photo | memory | color | brand | call_back | url


def get_html(URL, headers=HEADERS, params=' '):
    html = requests.get(URL, headers=headers, params=params)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup


def get_data(soup):
    items = soup.find_all('div', class_='M3v0L DUxBc sMgZR _5R9j6 qzGRQ IM66u J5vFR hxTp1')
    data = []
    for item in items:
        try:
            name = item.find('div', class_='M3v0L whAkJ mpcTk _0pTfu _0Jq1n sMgZR').find('span').get_text(strip=True).split(', ')[0]
            call_back = name.replace(' ', '_').lower()
        except:
            name = None
            call_back = None
        url = DOMEN + item.find('a', class_='_0cNvO jwtUM').get('href')
        

        try:
            price = item.find('span', class_='_3Trjq F7Tdh snf-- aXB7S uoQE-').get_text(strip=True).replace(' ','')[:-3]
        except:
            price = 0
        
        local_data = get_html(url)
        img = local_data.find('img', class_='MPQaS').get('src')
        description = local_data.find('div', class_='z1xg5').find('div').get_text(strip=True).replace("'", " ")
        if name is not None:
            data.append({
                'name': name,
                'description': description,
                'price': int(price),
                'photo': img,
                'call_back': call_back,
                'url': url
            })
        print(call_back)
    return data  

def parse(page):
    contents = []
    for page in range(1 , page+1):
        html = get_html(URL, params={'page': page})
        content = get_data(html)
        contents.extend(content)
        print(f"Страница {page} готово!")
    return contents

def add_products_db(items: list[dict]):
    for item in items:
        insert_product(
            name=item['name'],
            description=item['description'],
            price=item['price'],
            photo=item['photo'],
            call_back=item['call_back'],
            url=item['url'])
        print(f"{item['name']} добавлен в базу данных!")




items = parse(page=4)
add_products_db(items=items)
