import requests
import datetime


def weather(day, time):
    """return the wunderground weather data for the day and time passed through"""
    data = requests.get("http://api.wunderground.com/api/37d281e3f1931e1e/hourly10day/q/Ireland/Dublin.json").json()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday',
            'Wednesday', 'Thursday', 'Friday', 'Saturday']

    change = int(time) - int((datetime.datetime.now()).strftime("%H"))
    diff = (days[days.index((datetime.datetime.now()).strftime("%A")):].index(day)*24-1)+ change

    return data['hourly_forecast'][diff]['temp']['metric'], data['hourly_forecast'][diff]['wspd']['metric'], \
           data['hourly_forecast'][diff]['icon_url'], int(data['hourly_forecast'][diff]['pop']), \
           data['hourly_forecast'][diff]['condition']