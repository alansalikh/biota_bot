from products import get_product_image, get_product, get_category

import requests
# get_product_image('http://127.0.0.1:8000/product')

# for product in get_products('http://127.0.0.1:8000/product/products'):
#     photo = f"media/{product['title']}"
#     # photo = open('gfg.png', 'rb')
#     description = product['description']
#     caption = f"{product['title']}\nЦена: {product['price']}\n{description}"
#     print(photo, caption)

# print([i['id'] for i in requests.get('http://127.0.0.1:8000/product/category/').json()])
# def j(data):
#     if data in [str(i['id']) for i in requests.get('http://127.0.0.1:8000/product/category/').json()]:
#         product = get_product(int(data))[0]
#         photo = f"media/{product['title']}.png"
#         photo = open(photo, 'rb')
#         description = product['description']
#         caption = f"{product['title']}\nЦена: {product['price']}\n{description}"
#         print(photo)
#         print(caption)

# j('1')
# data = {
#     'quantity': 1
# }
# r = requests.put('http://127.0.0.1:8000/user/cart/', data=data, )
# print(r.status_code, r.text)

# url = 'http://127.0.0.1:8000/user/user/'
# r = requests.get(url).json()
# print(r)
# for i in requests.get('http://127.0.0.1:8000/user/user/').json():
#     if i == None:
#         print('Error')
#     print('g')
#     print(i['chat_id'])
# if requests.get('http://127.0.0.1:8000/user/cart').json() == None:
#     print('Error')

# print(requests.get('http://127.0.0.1:8000/user/cart').json())


# url = 'http://127.0.0.1:8000/user/cart/'
# r = requests.delete(url+'15')
# print(r.status_code, r.text)

a = '2500.00'
print(a[:-3])