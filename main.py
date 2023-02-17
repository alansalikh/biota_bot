from db_users import cursor, conn
from telebot import types
import requests

def create_table_user():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(255) NOT NULL,
        first_name VARCHAR,
        last_name VARCHAR,
        chat_id INT);"""

    cursor.execute(query=query)
    conn.commit()
    print('create table users success!')
# create_table_user()
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
    url = 'http://164.90.224.228:/user/user/'
    r = requests.post(url=url, data=data)
    print(data, r.status_code)

def insert_in_cart(chat_id: str,
                   title: str,
                   price: str,
                   description: str,
                   image: str, 
                   quantity: int,):
    url = 'http://164.90.224.228:/user/cart/'
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

def update_cart(chat_id: str,
                   title: str,
                   price: str,
                   description: str,
                   image: str, 
                   quantity: int,
                   cart_id: str):
    url = f'http://164.90.224.228:/user/cart/{cart_id}/'
    data = {
        'user': int(chat_id),
        'title': title,
        'price': float(price),
        'description': description,
        'image': image,
        'quantity': quantity
    }
    r = requests.put(url=url, data=data)
    print(r.status_code, r.text)
# update_cart(2, 'Кыст аль хинди масло в капсулах Аль Ихлас.png', 3000, 'ихлас кыст', 'media/Кыст аль хинди масло в капсулах Аль Ихлас.png', 13, 1)
# insert_in_cart(1, 'Кыст аль Хинди Фаваид в капсулах', 2000, 'Кыст аль Хинди Фаваид в капсулах', 'media/Кыст аль Хинди Фаваид в капсулах.png')
# insert_user(phone_number='77476398516', first_name='алти', last_name='None', chat_id='1952483120')
# insert_user(
#     '46513346',
#     'first_name',
#     'last_name',
#     79486153
# )

def is_user_exists(chat_id: int) -> bool:
    users = requests.get('http://164.90.224.228:/user/user/').json()
    for user in users:
        if int(user['chat_id']) == chat_id:
            return False
    return True
# print(is_user_exists(852365236))

def create_inline_markup(row_width, kwargs= dict):
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    items = []
    for key, value in kwargs.items():
        item = types.InlineKeyboardButton(value, callback_data=key)
        items.append(item)
    markup.add(*items)
    return markup



