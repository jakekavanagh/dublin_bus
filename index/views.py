import json
import pandas as pd
import time as t
import datetime
import calendar
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .apps import IndexConfig
from .calculations.summary import summary_weather, raining
from .calculations.weather import weather
from .calculations.direct import direct, routey, bare
from .calculations.location import nearest
from .calculations.real_time import timetable
from .models import Averages, RoughAverages
from .models import Event_Api
from .models import Twitter

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
    print('\n\n')
    begin_total = t.clock()
    dicty = IndexConfig.dicty

    """parse the post data to get the variables entered by the user"""
    origin, destination, route, full_time, day = int(float(request.POST.get("orig", 0))), int(float(request.POST['dest'])), request.POST['route'], request.POST['time'], request.POST['day']
    full_time = full_time.strip('()')
    time, mins = full_time.split('.')
    time = int(time)
    """now we establish the direction the user is going in"""
    route_stripped = routey(route)
    direction = direct(origin, destination, dicty, route_stripped)
    bare_route = bare(route)
    """split the day into the word and number"""
    day_word = day[:-1]
    day_num = int(day[-1])

    """get the range of stops between the origin and destination stop"""
    start = dicty[route_stripped][str(direction)].index(str(origin))
    stop = dicty[route_stripped][str(direction)].index(str(destination))
    stops = dicty[route_stripped][str(direction)][start:stop]
    arrival = dicty[route_stripped][str(direction)][:start]

    """calling this function for the day entered by the user will return all the appropriate weather data"""
    begin = t.clock()
    temp, wspd, url, pop, condition = weather(day_word, time)
    end = t.clock()
    print("weather:", end-begin)


    """now we convert the summary data from string to a represented number"""
    summary = summary_weather(condition)

    """and we bin the rain from a percentage chance to a 0 or 1"""
    rain = raining(pop)

    """we create a dataframe for all the stops between the origin and destination, and a seperate dataframe for
    all the stops between the start of the route and the origin stop to train the model on"""
    columns = ['Avg', 'Temp', 'StopID', 'AtStop', 'Day', 'HourMin']
    hour_min = float(str(time)+'.'+str(mins))
    df = pd.DataFrame(columns=columns)

    begin = t.clock()
    asking = Averages.objects.filter(route=bare_route, direction=direction, stop__in=stops, day=day_num, hour=time)
    error_asking = RoughAverages.objects.filter(route=bare_route, direction=direction, stop__in=stops)
    for i in range(len(stops)):
        current_asking = asking.filter(stop=stops[i])
        try:
            current_asking = current_asking[0]
        except IndexError:
            current_asking = error_asking.filter(stop=stops[i])
            current_asking = current_asking[0]
            print("model 1 entered error handling")
        df.loc[i] = [current_asking.average, temp, stops[i], current_asking.at_stop, day_num, hour_min]
    end = t.clock()
    print("time to create df1 with length", df.shape[0], ":", end-begin)
    complete = IndexConfig.complete_model
    val = complete.predict(df)
    total = sum(val)/60

    df2 = pd.DataFrame(columns=columns)
    if str(origin) == dicty[route_stripped][str(direction)][0]:
        arrival_total = 0
    else:
        begin = t.clock()
        asking = Averages.objects.filter(route=bare_route, direction=direction, stop__in=arrival, day=day_num, hour=time)
        error_asking = RoughAverages.objects.filter(route=bare_route, direction=direction, stop__in=arrival)
        for i in range(len(arrival)):
            current_asking = asking.filter(stop=arrival[i])
            try:
                current_asking = current_asking[0]
            except:
                current_asking = error_asking.filter(stop=arrival[i])
                current_asking = current_asking[0]
                print("model 2 entered error handling")
            df2.loc[i] = [current_asking.average, temp, arrival[i], current_asking.at_stop, day_num, hour_min]
        end = t.clock()
        print("time to create df2 with length", df2.shape[0], ":", end-begin)
        val2 = complete.predict(df2)
        arrival_total = sum(val2)/60

    """we now can get the latitude and longitude from a seperate json file for the stops entered to mark on the map"""
    all_stops = IndexConfig.locations
    origin_lat, origin_lon = all_stops[str(origin)]["Lat"], all_stops[str(origin)]["Lon"]
    destination_lat, destination_lon = all_stops[str(destination)]["Lat"], all_stops[str(destination)]["Lon"]

    begin = t.clock()
    # Use for checking when there's no tweets for the day, checks the day before
    # today_date = datetime.date.today() - datetime.timedelta(days=1)

    # Query Twitter table for any road disruption updates. Time-range set to 3 hours from current time
    today_date = datetime.date.today()
    tweet_timerange = (datetime.datetime.now() - datetime.timedelta(hours=3)).time()

    try:
        twitter_results = serializers.serialize("json", Twitter.objects.filter(
            tweet_date=today_date, tweet_time__gte=tweet_timerange))
    except ObjectDoesNotExist:
        print("Object does not exist.")

        # Query for Event API table to retrieve event list for today
    today_name = str(calendar.day_name[(datetime.date.today()).weekday()])
    try:
        events = serializers.serialize("json", Event_Api.objects.filter(weekday=today_name))
    except ObjectDoesNotExist:
        print("Object does not exist.")
        end = t.clock()
        print("twitter:", end-begin)

    # event_results = event_parser(day)
    # event_json_data_string = json.dumps(event_results)
    times = str(timetable(bare_route, direction, arrival_total, time, day_word, mins))
    origin_word, destination_word = all_stops[str(origin)]['name'], all_stops[str(destination)]['name']
    context = {
        'origin': origin, 'origin_word': origin_word, 'destination': destination, 'destination_word': destination_word,
        'route': route, 'time': time, 'day': day_word, 'mins': mins,
        'pred': ("%.2f" % total), 'arrival': arrival_total, 'time_arrival': times,
        'origin_lat': origin_lat, 'origin_lon': origin_lon,
        'destination_lat': destination_lat, 'destination_lon': destination_lon,
        'temp': temp, 'wspd': wspd, 'url': url, 'events': events, 'tweet': twitter_results,
    }
    end_total = t.clock()
    print('total:', end_total-begin_total, '\n\n')
    return render(request, "index/detail.html", context)


def find(request):
    all_stops = IndexConfig.locations
    current = request.POST["current"]
    temp, wspd, url, pop, condition = weather(t.strftime("%A"), t.strftime("%H"))
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

