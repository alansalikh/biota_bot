from telebot import types
import requests

from config import product_link, cart_link, category_link, user_link


def insert_user(
                phone_number: str,
                first_name: str,
                last_name: str,
                chat_id: int):
    data = {
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'chat_id': chat_id,
    }
    url = user_link
    r = requests.post(url=url, data=data)
    print(data, r.status_code)

def insert_in_cart(chat_id: str,
                   title: str,
                   price: str,
                   description: str,
                   image: str, 
                   quantity: int,):
    url = cart_link
    data = {
        'user': int(chat_id),
        'title': title,
        'price': float(price),
        'description': description,
        'image': image,
        'quantity': quantity
    }
    r = requests.post(url=url, data=data)
    print(r.status_code, r.text)

def update_cart(chat_id: int,
                   title: str,
                   price: str,
                   description: str,
                   image: str, 
                   quantity: int,
                   cart_id: str):
    url = cart_link + f'{cart_id}/'
    print(url)
    data = {
        'user': chat_id,
        'title': title,
        'price': price,
        'description': description,
        'image': image,
        'quantity': quantity,
    }
    print(data)
    r = requests.put(url=url, json=data)
    print(r.status_code, r.text)

# update_cart('1495025177', 'КАЛЬЦИЙ - МАГНИЙ - ЦИНК от компании Balen.', '4500', """🌿Свойства: 

# - Кальций способствует укреплению костей и зубов.

# - Магний является компонентом костей и зубов.

# - Цинк участвует в поддержании многих биологических процессов, необходим для размножения клеток, что является процессом роста и восстановления.""", 'media/kaltsij-magnij-tsink-ot-kompanii-balen.png', 8, '2')


def is_user_exists(chat_id: int):
    users = requests.get(user_link).json()
    for user in users:
        if int(user['chat_id']) == chat_id:
            return False
    return True

def create_inline_markup(row_width, kwargs= dict):
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    items = []
    for key, value in kwargs.items():
        item = types.InlineKeyboardButton(value, callback_data=key)
        items.append(item)
    markup.add(*items)
    return markup



