import telebot
from telebot import types
import requests

from config import TOKEN, product_link, category_link, user_link, cart_link, admin_id
from main import insert_user, is_user_exists, create_inline_markup, insert_in_cart, update_cart
from products import get_product_image, get_category, get_user_id, get_product

bot = telebot.TeleBot(TOKEN)
products = {
            'title': None,
            'price': None,
            'description': None,
            'image': None,
            'chat_id': None,
            'cart_id': None,
                        }

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Зарегистрироваться', request_contact=True)
    markup.add(item1)

    text = "Здравствуйте это бот магазина Биота"
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact(message: types.Message):
    if message.contact is not None:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Продукты')
        item2 = types.KeyboardButton('Корзина')
        markup.add(item1, item2)

        if is_user_exists(message.chat.id):
            insert_user(
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name,
                last_name=message.contact.last_name,
                chat_id=message.chat.id
            )
            bot.send_message(message.chat.id, 'Вы успешно зарегистровались!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегистрованы!', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def text(message: types.Message):
    if message.chat.type == 'private':
        if message.text.lower() == 'продукты':
            category = get_category(category_link)      
            markup = create_inline_markup(row_width=3, kwargs=category)
            bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=markup)
        if message.text.lower() == 'корзина':
            if str(message.chat.id) in [i['chat_id'] for i in requests.get(user_link).json()]:
                for i in requests.get(user_link).json():
                    if i['chat_id'] == str(message.chat.id):
                        user_id = i['id']
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Оформить заказ')
                item2 = types.KeyboardButton('Вернуться в каталог')
                item3 = types.KeyboardButton('Корзина')
                markup.add(item1, item2, item3)
                bot.send_message(message.chat.id, text='Корзина:', reply_markup= markup)
                quantity = 0
                for i in requests.get(cart_link).json():
                    if str(i['user']) == str(user_id):
                        quantity += 1
                        product = i
                        
                        caption = f"{product['title']}\nЦена: {product['price'][:-3]}*{product['quantity']}={int(product['price'][:-3])*int(product['quantity'])}"
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton('Удалить из корзины', callback_data=f"delete_{product['id']}")
                        item2 = types.InlineKeyboardButton('Изменить количество', callback_data=f"change_{product['id']}")
                        markup.add(item1, item2)
                        bot.send_message(message.chat.id, text=caption, reply_markup=markup)   
                if quantity == 0:
                    bot.send_message(message.chat.id, text='Вы еще ничего не добавили в корзину')
            else:    
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Зарегистрироваться', request_contact=True)
                markup.add(item1)
                text = 'Вы не зарегистрированы, зарегистрируйтесь'
                bot.send_message(message.chat.id, text=text, reply_markup=markup)
            
        if message.text.lower() == 'вернуться в каталог':
            category = get_category(category_link)      
            markup = create_inline_markup(row_width=3, kwargs=category)
            bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=markup)

        if message.text.lower() == 'оформить заказ':
            text = ''
            price = 0
            user_id = get_user_id(message.chat.id)
            kol = 0
            phone_number = ''
            number_dict = {i['chat_id']:i['phone_number'] for i in requests.get(user_link).json()}
            for key, value in number_dict.items():
                if int(key) == message.chat.id:
                    phone_number = value
            
            for i in requests.get(cart_link).json():
                if str(i['user']) == str(user_id):
                    kol += 1
                    print(kol)
                    product = i
                    price = price + int(product['price'][:-3])*product['quantity']
                    text = text + f"{kol}) " + product['title'] + f" {product['price'][:-3]}*{product['quantity']}={int(product['price'][:-3])*int(product['quantity'])}₸" + '\n'
            w_text = text
            text = text + 'Общая сумма: ' + f"{price}₸"
            if kol == 0:
                bot.send_message(message.chat.id, 'Невозможно оформить заказ так как корзина пуста, добавьте товары в козину для оформления заказа')
            else:
                bot.send_message(message.chat.id, text)
                bot.send_message(admin_id, phone_number+'\n'+w_text)

            
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

        if call.message:
            if call.data in [str(i['id']) for i in requests.get(category_link).json()]:
                category = get_category(category_link)
                for i in range(1, len(category)+1):
                    if i == int(call.data):
                        categories = category[i]
                quantity = 0
                # for i in requests.get(product_link).json():
                #     if i['category'] == int(call.data):
                        # from pprint import pprint
                        # quantity += 1
                        # product = i
                        # caption = f"{product['title']}\nЦена: {product['price']}"
                        # markup = types.InlineKeyboardMarkup(row_width=2)
                        # call_back = product['call_back']
                        # item = types.InlineKeyboardButton(text='Добавить в корзину', callback_data=call_back)
                        # item1 = types.InlineKeyboardButton(text='Показать фото и описание', callback_data=f"photo_{call_back}")
                        # markup.add(item, item1)
                        # bot.send_message(call.message.chat.id, text=caption, reply_markup=markup)
                        # quantity += 1
                products_dict = get_product(product_link, call.data)
                print(products_dict)
                if get_product(product_link, call.data):
                    quantity += 1
                markup = create_inline_markup(1, products_dict)
                bot.send_message(call.message.chat.id, text=f'{categories}:', reply_markup=markup)
                if quantity == 0:
                    bot.send_message(call.message.chat.id, text='К сожелению в этой категории ничего нету')
                # category = get_category(category_link)      
                # markup = create_inline_markup(row_width=3, kwargs=category)
                # bot.send_message(call.message.chat.id, 'Выберите категорию:', reply_markup=markup)
            if call.data in [str(i['call_back']) for i in requests.get(product_link).json()]:
                for i in requests.get(product_link).json():
                    if i['call_back'] == call.data:
                        product = i
                        title = product['title']
                        price = product['price']
                        description = product['description']
                        image = f"media/{product['call_back']}.png"
                        for i in requests.get(user_link).json():
                            if i['chat_id'] == str(call.message.chat.id):
                                chat_id = i['id']
                        products['title'] = title
                        products['price'] = price
                        products['description'] = description
                        products['image'] = image
                        products['chat_id'] = chat_id
                        # insert_in_cart(products['chat_id'], products['title'], products['price'], products['description'], products['image'])

                        msg = bot.send_message(call.message.chat.id, text='Сколько штук?')
                        bot.register_next_step_handler(msg, quan)
            if call.data[:7] == 'delete_':
                cart_id = call.data[7::]
                url = cart_link
                requests.delete(url+cart_id)
                bot.send_message(call.message.chat.id, text='Товар успешно удален из вашей корзины')
            
            if call.data[:7] == 'change_':
                cart_id = call.data[7::]
                print(cart_id)
                for i in requests.get(user_link).json():
                    if str(i['chat_id']) == str(call.message.chat.id):
                        user_id = i['id']
                for i in requests.get(cart_link).json():
                    if str(i['id']) == str(cart_id):
                        print(i['id'])
                        product = i
                        print(product['image'])
                        title = product['title']
                        price = product['price']
                        description = product['description']
                        print(title)
                        image = product['image']
                        print(image)
                        products['title'] = title
                        products['price'] = price
                        products['description'] = description
                        products['image'] = image
                        products['chat_id'] = user_id
                        products['cart_id'] = cart_id
                        print(products)
                msg = bot.send_message(call.message.chat.id, 'Введите количество')
                bot.register_next_step_handler(msg, change_product)
            if call.data[:5] == 'text_':
                print(call.data[5:])
                product = call.data[5::]
                for i in requests.get(product_link).json():
                    if i['call_back'] == product:
                        description = i['description']
                        caption = f"{i['title']}\nЦена: {i['price']}\n{description}"
                        call_back = i['call_back']
                        callback_photo = "photo_" + i['call_back']
                        markup = types.InlineKeyboardMarkup(row_width=3)
                        callback =  "edit_" + str(i['category'])
                        item1 = types.InlineKeyboardButton(text='Назад', callback_data=callback)
                        item2 = types.InlineKeyboardButton(text='Добавить в корзину', callback_data=call_back)
                        item3 = types.InlineKeyboardButton(text='Показать фото', callback_data=callback_photo)
                        markup.add(item1, item2, item3)
                        media = types.InputMediaPhoto(media=photo, caption=caption)
                        print(media)
                        bot.edit_message_text(chat_id=call.message.chat.id, text=caption, reply_markup=markup, message_id=call.message.message_id)
            if call.data[:6] == 'photo_':
                call_back = call.data[6::]
                get_product_image(product_link)
                photo = f"media/{call_back}.png"
                photo = open(photo, 'rb') 
                for i in requests.get(product_link).json():
                    if i['call_back'] == call_back:
                        text = i['title']
                bot.send_photo(call.message.chat.id, photo=photo, caption=text)
            if call.data[:5] == 'edit_':
                print(call.data)
                categorys = call.data[5::]
                category = get_category(category_link)
                for i in range(1, len(category)+1):
                    if i == int(categorys):
                        categories = category[i]
                quantity = 0
                products_dict = get_product(product_link, categorys)
                if get_product(product_link, categorys):
                    quantity += 1
                markup = create_inline_markup(1, products_dict)
                print(call.message.message_id)
                text = f"{categories:}"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
                if quantity == 0:
                    bot.send_message(call.message.chat.id, text='К сожелению в этой категории ничего нету')
            # print(call.data)


def change_product(message):
    try:
        quantity = int(message.text)
        update_cart(products['chat_id'], products['title'], products['price'], products['description'], products['image'], quantity, products['cart_id'])
        print(quantity)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оформить заказ')
        item2 = types.KeyboardButton('Вернуться в каталог')
        item3 = types.KeyboardButton('Корзина')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Товар успешно обновлен', reply_markup=markup)
    except:
        msg = bot.send_message(message.chat.id, 'введите число!')
        bot.register_next_step_handler(msg, change_product)
    

def quan(message):
    try:
        update = True
        for i in requests.get(cart_link).json():
            if int(i['user']) == int(products['chat_id']) and str(i['title']) == str(products['title']):
                quantity = int(i['quantity'])+int(message.text)
                cart_id = i['id']
                update_cart(products['chat_id'], products['title'], products['price'], products['description'], products['image'], quantity, cart_id=cart_id)
                update = False
                break
        if update:
            quantity = int(message.text)
            insert_in_cart(products['chat_id'], products['title'], products['price'], products['description'], products['image'], quantity)
        print(update)

        markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item1 = types.KeyboardButton('корзина')
        item2 = types.KeyboardButton('оформить заказ')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, text='товар успешно добавлен в корзину!', reply_markup=markup)
    except:
        msg = bot.send_message(message.chat.id, 'введите число!')
        bot.register_next_step_handler(msg, quan)
    
            



bot.polling(non_stop=True)
