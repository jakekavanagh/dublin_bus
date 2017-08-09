import json
from .apps import IndexConfig
from .calculations.direct import routey
from django.shortcuts import render


def index(request):
    dicty = IndexConfig.dicty
    locations = IndexConfig.locations
    routes = []
    for i in dicty:
        routes += [routey(i)]
    hours = []
    for i in range(6, 24):
        hours += [str(i)]
    mins = []
    for i in range(0,60,5):
        i = str(i)
        if len(i) == 1:
            i = '0'+i
        mins += [i]
    context = {
        'routes': sorted(routes)[:-1],
        'hours': hours,
        'mins': mins,
        'dicty': json.dumps(dicty),
        'locations': json.dumps(locations),
    }
    return render(request, 'index/index.html', context)
