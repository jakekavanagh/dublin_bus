from django.apps import AppConfig
from time import sleep
from sklearn.externals import joblib
import os


class Call:
    x = "hi"
    def x(self):
        yz = joblib.load('./index/compress.pkl')
        print("only want to see this once")
        return yz


class IndexConfig(AppConfig):
    name = 'index'
    y = Call().x()
