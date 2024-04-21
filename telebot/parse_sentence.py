import spacy
import sklearn
from process_line import predict_line
from process_station import predict_station

import datetime
import dateparser
from rutimeparser import parse

from line_variants import LINE_VARIANTS
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from transformers import AutoTokenizer, AutoModel
import torch

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from transformers import AutoTokenizer, AutoModel


# Загрузка модели
nlp = spacy.load("sentence_model")

def process_query(query):
    doc = nlp(query)
    result = {}
    for ent in doc.ents:
        result[ent.label_] = ent.text
    print(result)
    return result


def parse_sting_date(date_string):
    result = dateparser.parse(date_string)
    if not result:
        result = parse(date_string)
    
    if isinstance(result, datetime.datetime):
        result = result.date()
    return result


def transform_query(query):
    reuslt = {'STATION': None, 'LINE': None, 'DATE': None}
    processed = process_query(query)
    if 'STATION' in processed.keys():
        reuslt['STATION'] = predict_station(processed['STATION'].capitalize())
    if 'LINE' in processed.keys():
        try:
            int(processed['LINE'])
            reuslt['LINE'] = int(processed['LINE'])
        except ValueError:
            reuslt['LINE'] = predict_line(processed['LINE'].capitalize())
    if 'LINE' in processed.keys():
        reuslt['DATE'] = parse_sting_date(processed['DATE'])
    print('функция выполнена', reuslt)
    return reuslt  


query = "сколько людей было на сходненской， 79 линия в прошлое воскресенье"
print(transform_query(query))