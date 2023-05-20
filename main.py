import telebot
from config import API_TOKEN
from telebot import types

import requests
from PIL import Image
from urllib.request import urlopen

global resultConnect

bot = telebot.TeleBot(API_TOKEN)


def connect(params):
    token = '8f7e6671-0ff8-41d7-a45c-b3dd32198698'
    url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword'
    try:
        r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token},
                         params=params)  # выполняем запрос
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        print(err)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Начать🎳",callback_data='start')
    markup.row(btn1)
    bot.send_message(message.chat.id, "Привет! Я бот который помогает выбирать подходящие фильмы по твоему запросу \n<b>Нажми кнопку 'Начать', чтобы подобрать фильм</b>",reply_markup=markup, parse_mode="html")
    bot.register_next_step_handler(message, on_click)

@bot.message_handler()
def on_click(message):
    bot.send_message(message.chat.id, 'Введите название фильма')
    resultConnect = connect(params= {'keyword': message.text, 'page': 1})
    photo = your_movie(resultConnect)
    bot.send_photo(chat_id=message.chat.id, photo=photo)
    bot.send_message(message.chat.id, 'Это тот фильм который вы выбрали?')
    bot.register_next_step_handler(message, after_choose_film)

@bot.message_handler()
def after_choose_film(message):
    if message.text.lower() == 'да':
        movie_results(message)
    if message.text.lower() == 'нет':
        pass

@bot.callback_query_handler(func=lambda callback: True)
def callback_start(callback):
    if callback.data == 'start':
        bot.send_message(callback.message.chat.id, 'Введите название фильма')


def your_movie(result):
    for i in range(len('films')):
        posterUrl = result['films'][i]['posterUrl']
        image = Image.open(urlopen(posterUrl))
        return image

# в целом можно вывести в кнопки, но пока сделаю, чтобы все сразу выводил
@bot.message_handler()
def movie_results(message):  # получаем представление данных в виде объекта Python
    # print(result)
    bot.send_message(message.chat.id, f'Фильм:, {resultConnect["films"][0]["nameRu"]}\n'
                                      f'Год выпуска:, {resultConnect["films"][0]["year"]}\n'
                                      f'Описание:, {resultConnect["films"][0]["description"]}\n'
                                      f'Рейтинг Кинопоиска:, {resultConnect["films"][0]["rating"]}')
bot.polling(none_stop=True)
