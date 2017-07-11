from django.shortcuts import render, get_object_or_404
from .models import Question, EventApi
from .apps import IndexConfig
import json
import pandas as pd

from django.views.generic.edit import CreateView, UpdateView



def index(request):
    dicty = IndexConfig.dicty
    arr = []
    for i in range(0, 24):
        arr += [str(i)]
    context = {
        'arr': arr,
        'stops': dicty['index'],
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
    df = pd.DataFrame(columns=columns)
    for i in range(len(stops)):
        df.loc[i] = [dicty[day_word][str(time)][str(stops[i])], 10.0, 33.0, stops[i], 0, 13, 1, day_num, time]

    df2 = pd.DataFrame(columns=columns)
    for i in range(len(arrival)):
        df2.loc[i] = [dicty[day_word][str(time)][str(stops[i])], 10.0, 33.0, stops[i], 0, 13, 1, day_num, time]

    x = IndexConfig.y
    val = x.predict(df)
    total = sum(val)/60

    val2 = x.predict(df2)
    arrival_total = sum(val2)/60
    print(arrival_total)

    with open('./index/static/index/karl.json') as data_file:
        karl_dict = json.load(data_file)
    origin_lat = karl_dict[str(origin)]["Lat"]
    origin_lon = karl_dict[str(origin)]["Lon"]
    destination_lat = karl_dict[str(destination)]["Lat"]
    destination_lon = karl_dict[str(destination)]["Lon"]

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
    }
    return render(request, "index/detail.html", context)





def student(request, question_text):
    question = get_object_or_404(Question, question_text=question_text)
    selected = request.POST["orig"]
    context = {
        "question": question,
        "selected": selected
    }
    return render(request, "detail/detail.html", context)
