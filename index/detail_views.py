import pandas as pd
import time as t
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .calculations.summary import summary_weather, raining
from .calculations.weather import weather
from .calculations.direct import direct, routey, bare
from .calculations.location import path
from .calculations.today import dayw
from .calculations.real_time import timetable
from .models import Averages, RoughAverages
from .models import Event
from .models import Twitter
from django.shortcuts import render
from .apps import IndexConfig
import datetime as dt


def detail(request):
    """import the json for the route as a dict"""
    print('\n\n')
    begin_total = t.clock()
    dicty = IndexConfig.dicty
    today = dayw()
    """parse the post data to get the variables entered by the user"""
    origin, destination, route, full_time, day = int(float(request.POST.get("orig", 0))),\
        int(float(request.POST.get('dest', request.POST.get("orig", 0)))), request.POST['route'], request.POST.get('time', '100'), request.POST.get('day', today)
    current = request.POST["current"]

    if full_time != '100':
        full_time = full_time.strip('()')
        time, mins = full_time.split('.')
        time = int(time)
    else:
        full_time = dt.datetime.now().time()
        time, mins = full_time.strftime("%H"), full_time.strftime("%M")
    """now we establish the direction the user is going in"""
    print("route is ", route)
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
    complete = IndexConfig.complete_model
    if origin == destination:
        total = 0
    else:
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
        val = complete.predict(df)
        total = sum(val)/60

    df2 = pd.DataFrame(columns=columns)
    print(origin, dicty[route_stripped][str(direction)][0])
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
    full_route, stop_names = path(stops, all_stops)
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

    # today_name = str(calendar.day_name[(datetime.date.today()).weekday()])

    try:
        events = serializers.serialize("json", Event.objects.filter(weekday=day_word))
    except ObjectDoesNotExist:
        print("Object does not exist.")
        end = t.clock()
        print("twitter:", end-begin)

    lat, lng = current.split(',')

    # event_results = event_parser(day)
    # event_json_data_string = json.dumps(event_results)
    print("arrival prediction", arrival_total)
    times = str(timetable(bare_route, direction, arrival_total, time, day_word, mins))
    origin_word, destination_word = all_stops[str(origin)]['name'], all_stops[str(destination)]['name']
    full_route = [[float(y) for y in x] for x in full_route]
    context = {
        'origin': origin, 'origin_word': origin_word, 'destination': destination, 'destination_word': destination_word,
        'route': route, 'time': time, 'day': day_word, 'mins': mins,
        'pred': ("%.2f" % total), 'arrival': arrival_total, 'time_arrival': times,
        'origin_lat': origin_lat, 'origin_lon': origin_lon,
        'destination_lat': destination_lat, 'destination_lon': destination_lon,
        'temp': temp, 'wspd': wspd, 'url': url, 'events': events, 'tweet': twitter_results, 'stops': full_route[1:],
        'names': stop_names, 'my_lat': lat, 'my_long': lng,
    }
    end_total = t.clock()
    print('total:', end_total-begin_total, '\n\n')
    return render(request, "index/detail.html", context)
