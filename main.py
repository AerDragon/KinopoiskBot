import telebot
from config import API_TOKEN
from telebot import types

import requests
from PIL import Image
from urllib.request import urlopen

global resultConnect
global film_id
global film_name
global number_of_similar_films

bot = telebot.TeleBot(API_TOKEN)

kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn1 = types.KeyboardButton(text="Да😎")
btn2 = types.KeyboardButton(text="Нет🥲")
kb.add(btn1,btn2)


def connect(params, url):
    token = '8f7e6671-0ff8-41d7-a45c-b3dd32198698'
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
    global resultConnect
    global film_name
    film_name = message.text
    resultConnect = connect(params= {'keyword': message.text, 'page': 1},url='https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword')
    photo = your_movie(resultConnect)
    bot.send_photo(chat_id=message.chat.id, photo=photo)
    bot.send_message(message.chat.id, 'Это тот фильм который вы выбрали?',reply_markup=kb)
    bot.register_next_step_handler(message, after_choose_film)


@bot.message_handler()
def after_choose_film(message):
    if message.text.lower() == 'да😎':
        movie_results(message)
    if message.text.lower() == 'нет🥲':
        bot.send_message(message.chat.id, "Введите /start для начала выбора другого фильма.", reply_markup=None)

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
    global resultConnect
    global film_id
    film_id = resultConnect['films'][0]['filmId']
    bot.send_message(message.chat.id, f'<b>Фильм</b>: {resultConnect["films"][0]["nameRu"]}\n'
                                      f'<b>Год выпуска</b>: {resultConnect["films"][0]["year"]}\n'
                                      f'<b>Описание</b>: {resultConnect["films"][0]["description"]}\n'
                                      f'<b>Рейтинг Кинопоиска</b>: {resultConnect["films"][0]["rating"]}\n'
                                      f'<b>ID Фильма на кинопоиске</b>: {film_id}', parse_mode="html")
    bot.send_message(message.chat.id, 'Хотите найти похожие фильмы?',reply_markup= kb)
    bot.register_next_step_handler(message, similar_films)

@bot.message_handler()
def similar_films(message):

    if message.text.lower() == "да😎":
        global film_id
        global film_name
        global number_of_similar_films

        result = connect(params={'keyword': film_name, 'page': 1}, url=f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}/similars")
        lst_of_id = [0]

        for i in range((result['total']) - int(0.4 * result['total'])):
            id = result['items'][i]['filmId']
            lst_of_id.append(id)
            num = str(i + 1) + '.'
            bot.send_message(message.chat.id, f'{num}{result["items"][i]["nameRu"]}')
        bot.send_message(message.chat.id,'Хотите ли узнать о каком-нибудь из фильмов подробнее?\nНапишите порядковый номер фильма',reply_markup=None)
        bot.register_next_step_handler(message,secondFilm,lst_of_id)
    else:
        bot.send_message(message.chat.id, "Тогда хорошего просмотра!")

@bot.message_handler()
def secondFilm(message, lst_of_id):
    global number_of_similar_films
    global film_name
    try:
        number_of_similar_films = lst_of_id[int(message.text)]
        result = connect(params={'keyword': film_name, 'page': 1},
                         url=f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{number_of_similar_films}')
        bot.send_message(message.chat.id, f"<b>Фильм</b>: {result['data']['nameRu']}\n"
                                          f"<b>Год выпуска</b>: {result['data']['year']}\n"
                                          f"<b>Описание</b>: {result['data']['description']}\n"
                                          f"<b>Url адрес</b>: {result['data']['webUrl']}",parse_mode="html", reply_markup=None)

    except TypeError:
        bot.send_message(message.chat.id, 'Пожалуйста укажите корректный номер')


bot.polling(none_stop=True)
