import telebot
from telebot import types, async_telebot
import asyncio
import json

from freezegun import freeze_time
from datetime import date

@freeze_time("2023-03-05")
def my_function():
    print(date.today())  # Выведет 2023-03-05

my_function()


import spacy
import sklearn
from process_line import predict_line
from process_station import predict_station

import datetime
import dateparser
from rutimeparser import parse

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from transformers import AutoTokenizer, AutoModel
import torch

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from transformers import AutoTokenizer, AutoModel

from parse_sentence import transform_query

import pandas as pd

# ____ Обработка чтения ____
df = pd.read_csv('Final_Stations.csv')

def format_date(date_obj):
    # Преобразуем дату в строку с возможными ведущими нулями
    formatted_date = date_obj.strftime('%m/%d/%Y')
    # Разбиваем строку по разделителям
    parts = formatted_date.split('/')
    # Убираем ведущие нули и собираем строку заново
    formatted_date = '/'.join(str(int(part)) for part in parts)
    return formatted_date

def query_data(df, station=None, date=None, line_name=None, line_num=None):
    # Проверяем наличие необходимых параметров
    missing_values = []
    if not station:
        missing_values.append("station")
    if not date:
        missing_values.append("date")
    if not (line_name or line_num):
        missing_values.append("line_name or line_num")
    
    # Возвращаем список отсутствующих параметров, если они есть
    if missing_values:
        return missing_values
    
    # Форматируем дату
    formatted_date = format_date(date)

    # Фильтруем данные по переданным параметрам
    if line_name:
        filtered_df = df.loc[(df['Line'] == line_name) & (df['Station'] == station), [formatted_date, 'Station', 'Line']]
    elif line_num:
        filtered_df = df.loc[(df['Number'] == line_num) & (df['Station'] == station), [formatted_date, 'Station', 'Number']]

    # Проверяем, нашли ли мы соответствующие записи в датафрейме
    if filtered_df.empty:
        return "На этой линии нет запрашиваемой станции"

    # Возвращаем данные
    return int(filtered_df[formatted_date].iloc[0])

# _____ Gодключение к боту _____

 
API_TOKEN = 'ваш токен'
bot = async_telebot.AsyncTeleBot(API_TOKEN)

# ______________________________________________________
# хранение состояния пользователя
user_state = {}
user_waiting_state = {}

# установление состояния пользователя
def set_user_state(user_id, state):
    user_state[user_id] = state

# установление списка недостающей информации для данного пользователя
def set_user_state(user_id, missing_info: list):
    user_state[user_id] = missing_info

# получение состояния пользователя
def get_user_state(user_id):
    return user_state.get(user_id, None)

# получение списка недостающей информации для данного пользователя
def get_user_state(user_id):
    return user_state.get(user_id, None)
# ______________________________________________________


# команда запуска бота
@bot.message_handler(commands=['start'])
async def handle_start(message):
    set_user_state(message.chat.id, 'choosing_general')

    # приветствующий текст
    start_text = "Привет, если тебя интересует пассажиропоток за какой-то день или период, то этот бот готов ответить"

    await bot.send_message(message.chat.id, start_text)



@bot.message_handler(content_types=['text'], func=lambda message: get_user_state(message.chat.id) == 'choosing_general')
async def get_text_messages(message):
    text = message.text

    transformed_query = transform_query(text)
    
    if isinstance(transformed_query['LINE'], int):
        lm = transformed_query['LINE']
        le = None
    else:
        le = transformed_query['LINE']
        lm = None
    
    print(le, lm)
    print(format_date(transformed_query['DATE']))
    print(transformed_query['STATION'])


    find_result = query_data(df, station=transformed_query['STATION'], date=transformed_query['DATE'], line_name=le, line_num=lm)

    if isinstance(find_result, list):
        return_text = f'Не хватает следующих данных'
    elif isinstance(find_result, int):
        return_text = f"{transformed_query['DATE']} пассажиропоток на станции {transformed_query['STATION']} на линии {transformed_query['LINE']} составил {find_result} человека"
    elif find_result == "На этой линии нет запрашиваемой станции":
        return_text = find_result

    await bot.send_message(message.chat.id, return_text)


# запуск бота
if __name__ == '__main__':
    asyncio.run(bot.polling())