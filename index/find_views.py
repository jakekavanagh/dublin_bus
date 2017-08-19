from .apps import IndexConfig
from .calculations.weather import weather
import time as t
from .calculations.location import nearest
from django.shortcuts import render



def find(request):
    all_stops = IndexConfig.locations
    current = request.POST.get("current", '')

    if current == '':
        # current = "53.343792,-6.254572"
        current = "53.3498,-6.2603"

    temp, wspd, url, pop, condition = weather(t.strftime("%A"), t.strftime("%H"))

    # Used for testing remmeber to remove
    # current = "6.2603, 53.3498"

    lat, lng = current.split(',')
    locations = nearest(lat, lng, all_stops)
    context = {
        'stop_1': locations[0][0], 'lat_1': locations[0][1], 'long_1': locations[0][2],
        'routes_1': [locations[0][0]]+[all_stops[locations[0][0]]['routes']], 'name_1': all_stops[locations[0][0]]['name'],
        'stop_2': locations[1][0], 'lat_2': locations[1][1], 'long_2': locations[1][2],
        'routes_2': [locations[1][0]]+[all_stops[locations[1][0]]['routes']], 'name_2': all_stops[locations[1][0]]['name'],
        'stop_3': locations[2][0], 'lat_3': locations[2][1], 'long_3': locations[2][2],
        'routes_3': [locations[2][0]]+[all_stops[locations[2][0]]['routes']], 'name_3': all_stops[locations[2][0]]['name'],
        'stop_4': locations[3][0], 'lat_4': locations[3][1], 'long_4': locations[3][2],
        'routes_4': [locations[3][0]]+[all_stops[locations[3][0]]['routes']], 'name_4': all_stops[locations[3][0]]['name'],
        'stop_5': locations[4][0], 'lat_5': locations[4][1], 'long_5': locations[4][2],
        'routes_5': [locations[4][0]]+[all_stops[locations[4][0]]['routes']], 'name_5': all_stops[locations[4][0]]['name'],
        'temp': temp, 'wspd': wspd, 'url': url,
        'my_lat': lat, 'my_long': lng,
    }
    return render(request, "index/find.html", context)
