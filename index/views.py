import json
import pandas as pd
from django.shortcuts import render
from .apps import IndexConfig
from .calculations.summary import summary_weather, raining
from .calculations.weather import weather
from .calculations.direct import direct


def index(request):
    dicty = IndexConfig.dicty
    arr = []
    for i in range(0, 24):
        arr += [str(i)]
    context = {
        'arr': arr,
        'stops': sorted(dicty['0']['index']+dicty['1']['index']),
               }
    return render(request, 'index/index.html', context)


def detail(request):
    """import the json for the route as a dict"""
    dicty = IndexConfig.dicty

    """parse the post data to get the variables entered by the user"""
    origin, destination, route, time, day = int(float(request.POST["orig"])), int(float(request.POST['dest'])),\
        int(float(request.POST['route'])),int(float(request.POST['time'])), request.POST['day']

    """now we establish the direction the user is going in"""
    direction = direct(origin, destination, dicty)

    """split the day into the word and number"""
    day_word = day[:-1]
    day_num = int(day[-1])

    """get the range of stops between the origin and destination stop"""
    start = dicty[str(direction)]['index'].index(origin)
    stop = dicty[str(direction)]['index'].index(destination)
    stops = dicty[str(direction)]['index'][start:stop]
    arrival = dicty[str(direction)]['index'][:start]

    """calling this function for the day entered by the user will return all the appropriate weather data"""
    temp, wspd, url, pop, condition = weather(day_word, time)

    """now we convert the summary data from string to a represented number"""
    summary = summary_weather(condition)

    """and we bin the rain from a percentage chance to a 0 or 1"""
    rain = raining(pop)

    """we create a dataframe for all the stops between the origin and destination, and a seperate dataframe for
    all the stops between the start of the route and the origin stop to train the model on"""
    columns = ['Avg', 'Temp', 'Wind_Speed', 'StopID', 'AtStop', 'Summary', 'Day', 'Hour', 'Rain', 'Direction']
    df = pd.DataFrame(columns=columns)
    for i in range(len(stops)):
        df.loc[i] = [dicty[str(direction)][str(day_num)][str(time)][str(stops[i])], temp, wspd, stops[i], 0, summary, day_num, time, rain, direction]
    df2 = pd.DataFrame(columns=columns)
    for i in range(len(arrival)):
        df2.loc[i] = [dicty[str(direction)][str(day_num)][str(time)][str(stops[i])], temp, wspd, stops[i], 0, summary, day_num, time, rain, direction]
    x = IndexConfig.y
    """val1 is the prediction of origin to destination and val2 is the prediction from terminal to origin"""
    val = x.predict(df)
    total = sum(val)/60
    val2 = x.predict(df2)
    arrival_total = sum(val2)/60

    """we now can get the latitude and longitude from a seperate json file for the stops entered to mark on the map"""
    with open('./index/static/index/karl.json') as data_file:
        karl_dict = json.load(data_file)
    origin_lat, origin_lon = karl_dict[str(origin)]["Lat"], karl_dict[str(origin)]["Lon"]
    destination_lat, destination_lon = karl_dict[str(destination)]["Lat"], karl_dict[str(destination)]["Lon"]

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
    with open('./index/static/index/karl.json') as data_file:
        karl_dict = json.load(data_file)
    current = request.POST["current"]
    print(current)
    # find_closest_neighbours(current, karl_dict)
    context = {
        'json': karl_dict,
    }
    return render(request, "index/findlocation.html", context)


