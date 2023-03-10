import urllib.request
from PIL import Image
import requests

from config import product_link, user_link

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
    url = product_link
    products = requests.get(url).json()
    product_list = []
    for product in products:
        if product['category'] == category:
            product_list.append(product)
    return product_list


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
        