# Telebot_npl
Телебот, который читает текстовые запросы пользователей о пассажиропотоке в метро за какой-то день в произвольном формате 

Ссылка на бота: https://t.me/IshikiIbot

Ссылка на презентацию (также прикреплена в pdf формате): https://docs.google.com/presentation/d/1VVbtuqIIK9Vf3s9PrVYaKr_88_G2VlquKsIlLuFwXrY/edit?usp=sharing

## Описание файлов

- **telebot.py** — Основной файл телеграм-бота для интерактивного доступа к функциям проекта.
- **Final_Stations.csv** — Датасет, содержащий данные о пассажиропотоке на станциях метро.
- **line_train.ipynb** — Ноутбук для обучения модели распознавания названий линий метро.
- **line_variants.py** — Датасет для обучения модели классификации линий метро.
- **station_train.ipynb** и **station_variants.py** — Ноутбуки и датасеты для обучения модели классификации станций метро.
- **.joblib файлы** — Сохраненные обученные модели для быстрой загрузки и использования.
- **train_sentences.py** — Датасет для обучения модели выделения информации из текста.
- **train_string.ipynb** — Ноутбук для обучения модели распознавания предложений.
- **parse_sentence.py**, **process_line.py**, **process_station.py** — Модули для обработки текста, приведения данных к нужному формату и их агрегации.

## Предварительная подготовка

Перед запуском бота необходимо обучить модели, используемые в проекте. Для этого следует выполнить следующие шаги:

1. Запустите ноутбуки `line_train.ipynb` и `station_train.ipynb` для обучения моделей распознавания линий и станций метро соответственно.
2. Обучите модель для выделения информации из текста с помощью ноутбука `train_string.ipynb`.

Эти шаги необходимы для корректной работы бота, так как они подготавливают все необходимые модели для дальнейшего анализа и запросов.

## Запуск

После обучения моделей запустите `telebot.py` для активации телеграм-бота, который будет взаимодействовать с пользователем и предоставлять информацию по запросам.
