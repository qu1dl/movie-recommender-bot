import telebot
from telebot import types
import random
import requests
import json
import sqlite3


header = {'x-api-key': 'YOUR API'}
request_films1 = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films?order=NUM_VOTE&type=FILM&ratingFrom=7&ratingTo=10&yearFrom=1000&yearTo=3000&page=5', headers=header)
request_films2 = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films?order=NUM_VOTE&type=FILM&ratingFrom=7&ratingTo=10&yearFrom=1000&yearTo=3000&page=4',headers=header)
request_films3 = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films?order=NUM_VOTE&type=FILM&ratingFrom=7&ratingTo=10&yearFrom=1000&yearTo=3000&page=3',headers=header)


json_films1 = json.loads(request_films1.text)
json_films2 = json.loads(request_films2.text)
json_films3 = json.loads(request_films3.text)

for i in json_films1['items']:
    id = i['kinopoiskId']
    request_id = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}', headers=header)
    json_id = json.loads(request_id.text)
    if json_id['kinopoiskId'] == i['kinopoiskId']:
        i['description'] = json_id['description']
for i in json_films2['items']:
    id = i['kinopoiskId']
    request_id = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}', headers=header)
    json_id = json.loads(request_id.text)
    if json_id['kinopoiskId'] == i['kinopoiskId']:
        i['description'] = json_id['description']
for i in json_films3['items']:
    id = i['kinopoiskId']
    request_id = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}', headers=header)
    json_id = json.loads(request_id.text)
    if json_id['kinopoiskId'] == i['kinopoiskId']:
        i['description'] = json_id['description']

films = {}


for i in json_films1['items']:
    films[i['nameRu']] = [i['genres'][0]] + [i['ratingKinopoisk']] + [i['description']] + [i['posterUrl']] + [i['year']] # делаем словарь фильмов (фильм: [жанр, оценка, описание, постер])
for i in json_films2['items']:
    films[i['nameRu']] = [i['genres'][0]] + [i['ratingKinopoisk']] + [i['description']] + [i['posterUrl']] + [i['year']] # делаем словарь фильмов (фильм: [жанр, оценка, описание, постер])
for i in json_films3['items']:
    films[i['nameRu']] = [i['genres'][0]] + [i['ratingKinopoisk']] + [i['description']] + [i['posterUrl']] + [i['year']] # делаем словарь фильмов (фильм: [жанр, оценка, описание, постер])

lst_films = list(films)

temp_lst = [] #список для сохранения фильмов
bot = telebot.TeleBot('YOUR TOKEN')
watched = [] #просмотренные фильмы
API = 'YOUR API'


def database(message):

    connect = sqlite3.connect('users_ci.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users_login(
            id INTEGER PRIMARY KEY,
            watched TEXT
        )""")
    connect.commit()
    cursor.execute("SELECT id FROM users_login WHERE id = {}".format(message.from_user.id))
    data = cursor.fetchone()
    if data is None:
        cursor.execute('INSERT INTO users_login (id) VALUES (?)', (message.from_user.id,))
        connect.commit()
        connect.close()



@bot.message_handler(commands=['film'])
def film(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_first = types.KeyboardButton('Посоветуй другой фильм')
    btn_second = types.KeyboardButton('Главное меню')
    btn_third = types.KeyboardButton('Хочу посмотреть')
    markup.row(btn_first, btn_second)
    markup.row(btn_third)
    a = random.choice(lst_films)
    try:
        bot.send_photo(message.chat.id, photo=films[a][3])
        bot.send_message(message.chat.id,
                         f'{a}\nГод {films[a][4]}\nЖанр {films[a][0]['genre']}\n Рейтинг {films[a][1]}\n Описание: {films[a][2]}',
                         reply_markup=markup)
    except:
        bot.send_message(message.chat.id,
                         f'{a}\nГод {films[a][4]}\nЖанр {films[a][0]['genre']}\n Рейтинг {films[a][1]}\n Описание: {films[a][2]}',
                         reply_markup=markup)
    temp_lst.append(a)
    bot.register_next_step_handler(message,main)


@bot.message_handler(commands=['help'])
def helping(message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Главное меню')
    mark.row(button)
    bot.send_message(message.chat.id, 'По всем вопросам обращаться к @Jshjeo', reply_markup=mark)
    bot.register_next_step_handler(message, start)


@bot.message_handler(commands=['start'])
def start(message):
    database(message)
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Выбор фильма')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Список желаемого')
    start_markup.row(btn1,btn2)
    start_markup.row(btn3)
    bot.send_message(message.chat.id,f'Привет, {message.from_user.first_name}\nДанный бот может помочь тебе в поисках хорошего фильма\n'
                                     f'Бот рекомендует фильмы с рейтингом не ниже 7.0\n/help - если возникли вопросы',reply_markup=start_markup)
    bot.register_next_step_handler(message,start_click)


def start_click(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_first = types.KeyboardButton('Посоветуй другой фильм')
    btn_second = types.KeyboardButton('Главное меню')
    btn_third = types.KeyboardButton('Хочу посмотреть')
    markup.row(btn_first, btn_second)
    markup.row(btn_third)
    if message.text == 'Выбор фильма':
        a = random.choice(lst_films)
        try:
            bot.send_photo(message.chat.id, photo=films[a][3])
            bot.send_message(message.chat.id,
                             f'{a}\nГод {films[a][4]}\nЖанр {films[a][0]['genre']}\n Рейтинг {films[a][1]}\n Описание: {films[a][2]}',
                             reply_markup=markup)
        except:
            bot.send_message(message.chat.id,
                             f'{a}\nГод {films[a][4]}\nЖанр {films[a][0]['genre']}\n Рейтинг {films[a][1]}\n Описание: {films[a][2]}',
                             reply_markup=markup)
        temp_lst.append(a)
        bot.register_next_step_handler(message,main)
    elif message.text == 'Помощь':
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Главное меню')
        mark.row(button)
        bot.send_message(message.chat.id,'По всем вопросам обращаться к @Jshjeo',reply_markup=mark)
        bot.register_next_step_handler(message, start)
    elif message.text.lower() == '/start':
        start(message)
    elif message.text.lower() == '/help':
        helping(message)
    elif message.text.lower() == '/film':
        film(message)
    elif message.text == 'Список желаемого':
        mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Главное меню')
        button2 = types.KeyboardButton('Очистить')
        mark.row(button1,button2)

        connect = sqlite3.connect('users_ci.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users_login WHERE id = ?', (message.from_user.id,))
        existing_user = cursor.fetchall()
        for value in existing_user:
            if list(value)[1] == None:
                bot.send_message(message.chat.id,'Список пуст',reply_markup=mark)
            else:
                bot.send_message(message.chat.id,f'{list(value)[1]}',reply_markup=mark)
        connect.close()

    elif ((message.text != 'Список желаемого') or (message.text != 'Выбор фильма') or (message.text != 'помощь')
          or (message.text.lower() != '/help') or (message.text.lower() != '/start') or (message.text.lower() != '/film')
          or (message.text.lower() != 'очистить')):
        start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Выбор фильма')
        btn2 = types.KeyboardButton('Помощь')
        btn3 = types.KeyboardButton('Просмотренные фильмы')
        start_markup.row(btn1, btn2)
        start_markup.row(btn3)
        bot.send_message(message.chat.id,'Неверная команда',reply_markup=start_markup)
        bot.register_next_step_handler(message,start_click)


@bot.message_handler()
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_first = types.KeyboardButton('Посоветуй другой фильм')
    btn_second = types.KeyboardButton('Главное меню')
    btn_third = types.KeyboardButton('Хочу посмотреть')
    markup.row(btn_first, btn_second)
    markup.row(btn_third)
    if message.text == 'Посоветуй другой фильм':
        a = random.choice(lst_films)
        try:
            bot.send_photo(message.chat.id, photo=films[a][3])
            bot.send_message(message.chat.id,
                             f'{a}\nГод {films[a][4]}\nЖанр {films[a][0]['genre']}\n Рейтинг {films[a][1]}\n Описание: {films[a][2]}',
                             reply_markup=markup)
        except:
            bot.send_message(message.chat.id,
                             f'{a}\nГод {films[a][4]}\nЖанр {films[a][0]['genre']}\n Рейтинг {films[a][1]}\n Описание: {films[a][2]}',
                             reply_markup=markup)
        temp_lst.append(a)

    elif message.text.lower() == '/start':
        start(message)
    elif message.text.lower() == '/help':
        helping(message)
    elif message.text.lower() == '/film':
        film(message)
    elif message.text == 'Главное меню':
        start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Выбор фильма')
        btn2 = types.KeyboardButton('Помощь')
        btn3 = types.KeyboardButton('Список желаемого')
        start_markup.row(btn1, btn2)
        start_markup.row(btn3)
        bot.send_message(message.chat.id,
                         f'Привет, {message.from_user.first_name}\nДанный бот может помочь тебе в поисках хорошего фильма\n'
                         f'Бот рекомендует фильмы с рейтингом не ниже 7.0\n/help - если возникли вопросы',
                         reply_markup=start_markup)
        bot.register_next_step_handler(message, start_click)
    elif message.text == 'Хочу посмотреть':
        watched.append(temp_lst[-1])
        connect = sqlite3.connect('users_ci.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM users_login WHERE id = ?', (message.from_user.id,))
        existing_user = cursor.fetchone()
        if existing_user:
            watched_film = watched[-1]
            updated_films = existing_user[1] + ', ' + watched_film if existing_user[1] else watched_film
            cursor.execute('UPDATE users_login SET watched = ? WHERE id = ?', (updated_films, message.from_user.id))
            connect.commit()
            connect.close()
            temp_lst.clear()
        else:
            cursor.execute('INSERT INTO users_login (id) VALUES (?)', (message.from_user.id,))
            connect.commit()
            connect.close()
        bot.send_message(message.chat.id, f'Фильм добавлен в желаемое')
    elif message.text.lower() == 'очистить':
        connect = sqlite3.connect('users_ci.db')
        cursor = connect.cursor()
        cursor.execute('UPDATE users_login SET watched = ? WHERE id = ?', (None, message.from_user.id))
        connect.commit()
        connect.close()
        bot.send_message(message.chat.id, 'Список очищен')
    elif ((message.text != 'Хочу посмотреть') or (message.text != 'Главное меню') or (message.text != 'Посоветуй другой фильм')
          or (message.text.lower() != '/help') or (message.text.lower() != '/start')
          or (message.text.lower() != '/film') or (message.text.lower() != 'очистить')):
        wrong_mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_one = types.KeyboardButton('Посоветуй другой фильм')
        button_two = types.KeyboardButton('Главное меню')
        wrong_mark.row(button_one,button_two)
        bot.send_message(message.chat.id,'Неверная команда',reply_markup=wrong_mark)


bot.polling(none_stop=True)
