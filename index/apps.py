from django.apps import AppConfig
from sklearn.externals import joblib
import json


def model():
    model = joblib.load('./index/static/index/random_forest_regressor.pkl')
    return model


def dicty():
    with open('./index/static/index/stops_in_order.json') as data_file:
        dicty = json.load(data_file)
    return dicty


def locations():
    with open('./index/static/index/lats_and_longs.json') as data_file:
        locations = json.load(data_file)
    return locations


class IndexConfig(AppConfig):
    name = 'index'
    # y = x()
    complete_model = model()
    dicty = dicty()
    # route1 = route1()
    locations = locations()

