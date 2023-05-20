import requests
from PIL import Image
from urllib.request import urlopen
import json
import pandas as pd

import main

# поиск ID фильма
token = '8f7e6671-0ff8-41d7-a45c-b3dd32198698'
url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword'
params = {'keyword': main.reply_message, 'page': 1}
def connect():
    try:
        r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token},
                         params=params)  # выполняем запрос
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token}, params=params)

# In[40]:


result = r.json()


def your_movie():
    for i in range(len('films')):
        posterUrl = result['films'][i]['posterUrl']
        image = Image.open(urlopen(posterUrl))
        return image


def movie_results(film_id):
    result = r.json()  # получаем представление данных в виде объекта Python
    # print(result)
    film_id = result['films'][0]['filmId']

    print('Фильм:', result['films'][0]['nameRu'])
    print('Год выпуска:', result['films'][0]['year'])
    print('Описание:', result['films'][0]['description'])
    print('Рейтинг Кинопоиска:', result['films'][0]['rating'])
    print(film_id)


film_id = result['films'][0]['filmId']
movie_results(film_id)


# In[42]:


def similar_films(url):
    # similar films
    url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}/similars"
    params = {'page': 1}

    r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token}, params=params)


url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}/similars"
similar_films(url)

# In[43]:


r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token}, params=params)
connect(r)

# In[44]:


result = r.json()


def similar_films_result(id):
    result = r.json()
    # print(result)
    lst_of_id = [0]
    for i in range((result['total']) - int(0.4 * result['total'])):
        id = result['items'][i]['filmId']
        lst_of_id.append(id)
        num = str(i + 1) + '.'
        print(num, result['items'][i]['nameRu'])
        # print(lst_of_id)


id = result['items'][i]['filmId']
similar_films_result(id)


# In[47]:


def want_more(answer1):
    print('Хотите узнать подробнее о каком-нибудь фильме?', 'Напишите порядковый номер фильма или "нет"', sep='\n')
    answer1 = str(input()).lower()
    if answer1 == 'нет':
        quit
    else:
        id = lst_of_id[int(answer1)]


want_more(answer1)
answer1 = str(input()).lower()


# In[48]:


def second_movie(result):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{id}'
    params = {'page': 1}
    r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token}, params=params)
    try:
        r = requests.get(url, headers={'accept': 'application/json', "X-API-KEY": token},
                         params=params)  # выполняем запрос
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    # print(r.headers)
    result = r.json()
    # print(result)
    print('Фильм:', result['data']['nameRu'])
    print('Год выпуска:', result['data']['year'])
    print('Описание:', result['data']['description'])
    print('Продолжительность:', result['data']['filmLength'])


result = r.json()
second_movie(result)