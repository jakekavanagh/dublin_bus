from django.shortcuts import render
from .apps import IndexConfig


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

