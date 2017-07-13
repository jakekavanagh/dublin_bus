from django.shortcuts import render, get_object_or_404
from .apps import IndexConfig
import json
import pandas as pd
import requests
import datetime


def weather(day, time):
    data = requests.get("http://api.wunderground.com/api/37d281e3f1931e1e/hourly10day/q/Ireland/Dublin.json").json()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday',
            'Wednesday', 'Friday', 'Saturday']

    change = time - int((datetime.datetime.now()).strftime("%H"))
    diff = (days[days.index((datetime.datetime.now()).strftime("%A")):].index(day)*24-1)+ change

    return data['hourly_forecast'][diff]['temp']['metric'], data['hourly_forecast'][diff]['wspd']['metric'], \
        data['hourly_forecast'][diff]['icon_url']


def index(request):
    dicty = IndexConfig.dicty
    arr = []
    for i in range(0, 24):
        arr += [str(i)]
    context = {
        'arr': arr,
        'stops': sorted(dicty['index']),
               }
    return render(request, 'index/index.html', context)


def detail(request):
    dicty = IndexConfig.dicty
    origin, destination, route, time, day = int(float(request.POST["orig"])), int(float(request.POST['dest'])),\
        int(float(request.POST['route'])),int(float(request.POST['time'])), request.POST['day']
    day_word = day[:-1]
    day_num = int(day[-1])
    start = dicty['index'].index(origin)
    stop = dicty['index'].index(destination)
    stops = dicty['index'][start:stop]
    arrival = dicty['index'][:start]
    columns = ['Avg', 'Temp', 'Wind_Speed', 'StopID', 'AtStop', 'Summary', 'Rain', 'Day', 'Hour']
    temp, wspd, url = weather(day_word, time)
    df = pd.DataFrame(columns=columns)
    for i in range(len(stops)):
        df.loc[i] = [dicty[day_word][str(time)][str(stops[i])], temp, wspd, stops[i], 0, 13, 1, day_num, time]

    df2 = pd.DataFrame(columns=columns)
    for i in range(len(arrival)):
        df2.loc[i] = [dicty[day_word][str(time)][str(stops[i])], temp, wspd, stops[i], 0, 13, 1, day_num, time]

    x = IndexConfig.y
    val = x.predict(df)
    total = sum(val)/60

    val2 = x.predict(df2)
    arrival_total = sum(val2)/60

    with open('./index/static/index/karl.json') as data_file:
        karl_dict = json.load(data_file)
    origin_lat = karl_dict[str(origin)]["Lat"]
    origin_lon = karl_dict[str(origin)]["Lon"]
    destination_lat = karl_dict[str(destination)]["Lat"]
    destination_lon = karl_dict[str(destination)]["Lon"]
    print(url)
    context = {
        'origin': origin,
        'destination': destination,
        'route': route,
        'time': time,
        'day': day_word,
        'pred': total,
        'arrival': arrival_total,
        'origin_lat': origin_lat,
        'origin_lon': origin_lon,
        'destination_lat': destination_lat,
        'destination_lon': destination_lon,
        'temp': temp,
        'wspd': wspd,
        'url': url,
    }
    return render(request, "index/detail.html", context)

def find(request):
    return render(request, "index/findlocation.html")


def indexmobile(request):
    dicty = IndexConfig.dicty
    arr = []
    for i in range(0, 24):
        arr += [str(i)]
    context = {
        'arr': arr,
        'stops': sorted(dicty['index']),
    }
    return render(request, 'index/indexmobile.html', context)

