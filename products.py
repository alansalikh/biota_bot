# id | name | description | price | photo | memory | color |brand | call_back | url
from db_product import conn, cursor
import urllib.request
from PIL import Image
from telebot import types
import telebot
import requests

def create_table_product():
    query = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR,
            description TEXT,
            price INT,
            photo VARCHAR,
            call_back VARCHAR,
            url VARCHAR);"""
    cursor.execute(query=query)
    conn.commit()

def insert_product(name: str, 
                  description: str, 
                  price: int, 
                  photo: str, 
                  call_back: str,
                  url: str):
    query = f"""
        INSERT INTO products (
            name, description, price, photo, call_back, url
        )VALUES (
            '{name}', '{description}', {price}, '{photo}', '{call_back}', '{url}'
        );"""
    cursor.execute(query=query)
    conn.commit()

    
def get_info(call_back: str):
    query = f"""
        SELECT * 
        FROM products
        where call_back = '{call_back}';"""

    cursor.execute(query=query)
    response = cursor.fetchall()
    return response

# def save_in_cart( )

def get_category(url):
    r = requests.get(url)
    datas = r.json()
    return {data['id']: data['title'] for data in datas}

def get_product_image(url):
    r = requests.get(url)
    datas = r.json()
    for data in datas:
        urllib.request.urlretrieve(data['image'], f"media/{data['title']}.png")
        image = Image.open(f"media/{data['title']}.png")
    return image

def get_product(category):
    url = 'http://164.90.224.228:8000/product/products'

    # categories = requests.get('http://164.90.224.228:8000/product/category/').json()
    # category_list = []
    # for category in categories:
    #     category_list.append(category['id'])

    products = requests.get(url).json()
    from pprint import pprint
    # pprint(r.json())
    product_list = []
    for product in products:
        if product['category'] == category:
            product_list.append(product)
# print(category_list)
    return product_list


def get_products(url):
    data = requests.get(url).json()
    if data:
        get_product_image(url)
        return data
    return None
# id | name | description | price | photo | memory | color | brand | call_back | url

def send_phone(call,  bot: telebot.TeleBot, phone: tuple):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Добавить в корзину', callback_data=phone[0])
    item2 = types.InlineKeyboardButton('Полная информация', url=phone[9])
    markup.add(item1,item2)
    image = get_product_image(phone[4])
    text = f"""
Телефон: {phone[1]}{phone[5]}
Цвет: {phone[6].title()}
Цена: {phone[3]} ₸
Описание: {phone[2]}
"""
    bot.send_photo(
            chat_id=call.message.chat.id,
            photo=image,
            caption=text,
            reply_markup=markup)


# from pprint import pprint

# pprint(get_info_phone(call_back='apple_iphone_11'))