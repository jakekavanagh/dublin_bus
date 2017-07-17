from django.apps import AppConfig
from sklearn.externals import joblib
import json


# class Call:
def x():
    yz = joblib.load('./index/bus 1 complete.pkl')
    return yz

def dicty():
    with open('./index/static/index/Bus_1.json') as data_file:
        dicty = json.load(data_file)
    return dicty



class IndexConfig(AppConfig):
    name = 'index'
    y = x()
    dicty = dicty()
