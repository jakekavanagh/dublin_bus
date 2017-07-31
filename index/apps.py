from django.apps import AppConfig
from sklearn.externals import joblib
import json


def model():
    model = joblib.load('./index/twentyextra time feature.pkl')
    return model


# def route1():
#     with open('./index/static/index/Bus_1.json') as data_file:
#         dicty = json.load(data_file)
#     return dicty


def dicty():
    with open('./index/static/index/stops in order.json') as data_file:
        dicty = json.load(data_file)
    return dicty


def locations():
    with open('./index/static/index/BusStop_Locations with names.json') as data_file:
        locations = json.load(data_file)
        return locations


class IndexConfig(AppConfig):
    name = 'index'
    # y = x()
    complete_model = model()
    dicty = dicty()
    # route1 = route1()
    locations = locations()

