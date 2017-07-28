import json
import pandas as pd
from django.shortcuts import render
from .apps import IndexConfig
from .calculations.summary import summary_weather, raining
from .calculations.weather import weather
from .calculations.direct import direct, routey
from .calculations.location import nearest
from .calculations.real_time import timetable
from .calculations.AARoadWatch_Alert import connection_twitter
import time
from .models import Averages, RoughAverages
from django.core.exceptions import ObjectDoesNotExist
# from .calculations.events import event_parser


def index(request):
    dicty = IndexConfig.dicty
    routes = []
    for i in dicty:
        routes += [routey(i)]
    hours = []
    for i in range(6, 23):
        hours += [str(i)]
    mins = []
    for i in range(0,60,5):
        i = str(i)
        if len(i) == 1:
            i = '0'+i
        mins += [i]
    context = {
        'routes': sorted(routes),
        'hours': hours,
        'mins': mins,
        'dicty': json.dumps(dicty),
    }
    return render(request, 'index/index.html', context)


def detail(request):
    """import the json for the route as a dict"""
    dicty = IndexConfig.dicty

    """parse the post data to get the variables entered by the user"""
    origin, destination, route, full_time, day = int(float(request.POST["orig"])), int(float(request.POST['dest'])),\
        int(float(request.POST['route'])), request.POST['time'], request.POST['day']
    full_time = full_time.strip('()')
    time, mins = full_time.split('.')
    time = int(time)
    """now we establish the direction the user is going in"""
    route_stripped = routey(route)
    direction = direct(origin, destination, dicty, route_stripped)

    """split the day into the word and number"""
    day_word = day[:-1]
    day_num = int(day[-1])
    """get the range of stops between the origin and destination stop"""
    start = dicty[route_stripped][str(direction)].index(str(origin))
    stop = dicty[route_stripped][str(direction)].index(str(destination))
    stops = dicty[route_stripped][str(direction)][start:stop]
    arrival = dicty[route_stripped][str(direction)][:start]

    """calling this function for the day entered by the user will return all the appropriate weather data"""
    temp, wspd, url, pop, condition = weather(day_word, time)

    """now we convert the summary data from string to a represented number"""
    summary = summary_weather(condition)

    """and we bin the rain from a percentage chance to a 0 or 1"""
    rain = raining(pop)

    """we create a dataframe for all the stops between the origin and destination, and a seperate dataframe for
    all the stops between the start of the route and the origin stop to train the model on"""
    columns = ['Avg', 'Temp', 'StopID', 'AtStop', 'Day', 'HourMin']
    hour_min = float(str(time)+'.'+str(mins))
    df = pd.DataFrame(columns=columns)
    for i in range(len(stops)):
        try:
            asking = Averages.objects.get(route=str(route), direction=direction, stop=stops[i], day=day_num, hour=time)
        except ObjectDoesNotExist:
            asking = RoughAverages.objects.get(route=str(route), direction=direction, stop=stops[i])
        df.loc[i] = [asking.average, temp, stops[i], asking.at_stop, day_num, hour_min]
    complete = IndexConfig.complete_model
    val = complete.predict(df)
    total = sum(val)/60

    df2 = pd.DataFrame(columns=columns)
    if str(origin) == dicty[route_stripped][str(direction)][0]:
        arrival_total = 0
    else:
        for i in range(len(arrival)):
            try:
                asking = Averages.objects.get(route=str(route), direction=direction, stop=arrival[i], day=day_num, hour=time)
            except ObjectDoesNotExist:
                asking = Averages.objects.get(route=str(route), direction=direction, stop=arrival[i])
            print(asking)
            df2.loc[i] = [asking.average, temp, arrival[i], asking.at_stop, day_num, hour_min]
        val2 = complete.predict(df2)
        arrival_total = sum(val2)/60
        print(arrival_total)

    """we now can get the latitude and longitude from a seperate json file for the stops entered to mark on the map"""
    all_stops = IndexConfig.locations
    origin_lat, origin_lon = all_stops[str(origin)]["Lat"], all_stops[str(origin)]["Lon"]
    destination_lat, destination_lon = all_stops[str(destination)]["Lat"], all_stops[str(destination)]["Lon"]

    twitter_results = connection_twitter()
    twitter_json_data_string = json.dumps(twitter_results)

    # event_results = event_parser(day)
    # event_json_data_string = json.dumps(event_results)
    times = str(timetable(route, direction, arrival_total, time, day_word, mins))
    context = {
        'origin': origin, 'destination': destination,
        'route': route, 'time': time, 'day': day_word, 'mins': mins,
        'pred': ("%.2f" % total), 'arrival': arrival_total, 'time_arrival': times,
        'origin_lat': origin_lat, 'origin_lon': origin_lon,
        'destination_lat': destination_lat, 'destination_lon': destination_lon,
        'temp': temp, 'wspd': wspd, 'url': url,
        # 'events': event_json_data_string,
        'tweet': twitter_json_data_string,
    }
    return render(request, "index/detail.html", context)


def find(request):
    all_stops = IndexConfig.locations
    current = request.POST["current"]
    temp, wspd, url, pop, condition = weather(time.strftime("%A"), time.strftime("%H"))
    lat, lng = current.split(',')
    locations = nearest(lat, lng, all_stops)
    context = {
        'stop_1': locations[0][0], 'lat_1': locations[0][1], 'long_1': locations[0][2],
        'stop_2': locations[1][0], 'lat_2': locations[1][1], 'long_2': locations[1][2],
        'stop_3': locations[2][0], 'lat_3': locations[2][1], 'long_3': locations[2][2],
        'stop_4': locations[3][0], 'lat_4': locations[3][1], 'long_4': locations[3][2],
        'stop_5': locations[4][0], 'lat_5': locations[4][1], 'long_5': locations[4][2],
        'temp': temp, 'wspd': wspd, 'url': url,
        'my_lat': lat, 'my_long': lng,
    }
    return render(request, "index/find.html", context)


def indexmobile(request):
    dicty = IndexConfig.dicty
    arr = []
    for i in range(0, 24):
        arr += [str(i)]
    context = {
        'arr': arr,
        'stops': sorted(dicty['0']['index']+dicty['1']['index']),
    }
    return render(request, "index/indexmobile.html", context)

