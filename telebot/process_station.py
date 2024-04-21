from transformers import AutoTokenizer, AutoModel
import torch
from joblib import load

# Загружаем классификатор KNN и LabelEncoder
clf = load('stations_knn_classifier.joblib')
label_encoder = load('stations_label_encoder.joblib')

# Загружаем токенизатор
tokenizer = AutoTokenizer.from_pretrained('stations_tokenizer')

# Загружаем модель трансформера
model = AutoModel.from_pretrained('stations_rubert-tiny-model')


def get_embeddings(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=32)
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state[:, 0, :].numpy()  # Берем эмбеддинги первого токена [CLS]
    return embeddings


def predict_station(query):
    query_embedding = get_embeddings([query])
    prediction = clf.predict(query_embedding)
    return label_encoder.inverse_transform(prediction)[0]

