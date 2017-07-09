from django.apps import AppConfig
from time import sleep


class Call:
    x = "hi"
    def x(self):
        sleep(15)
        print("only want to see this once")
        return "hi"


class IndexConfig(AppConfig):
    name = 'index'
    y = Call().x()
