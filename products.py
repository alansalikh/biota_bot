import urllib.request
from PIL import Image
import requests
import os

from config import product_link, user_link

def get_category(url):
    r = requests.get(url)
    datas = r.json()
    return {data['id']: data['title'] for data in datas}

def get_product_image(url):
    r = requests.get(url)
    datas = r.json()
    for data in datas:
        folder = '/home/salikh/bot/biota_bot/media/'
        filename = f"{data['call_back']}"

        if not os.path.isfile(folder+filename):
            urllib.request.urlretrieve(data['image'], f"media/{data['call_back']}.png")

def get_product(url, category):
    r = requests.get(url)
    datas = r.json()
    product = {}
    for data in datas:
        if int(category) == data['category']:
            x = "text_" + data['call_back']
            product[x] = data['title']
    return product


def get_products(url):
    data = requests.get(url).json()
    if data:
        get_product_image(url)
        return data
    return None

def get_user_id(chat_id):
    for i in requests.get(user_link).json():
        if i['chat_id'] == str(chat_id):
            return i['id']
        