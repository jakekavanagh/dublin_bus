from .find_views import find
from .index_views import index
from .detail_views import detail
from .index_mobile_views import indexmobile

# from .models import Luas
# from .models import RealTime_Luas
from django.shortcuts import render
from django.core import serializers


# def luas(request):
#     luas_stops = serializers.serialize("json", Luas.objects.all())
#     luas_realtime = serializers.serialize("json", RealTime_Luas.objects.all())
#
#     context = {
#         'luas_stops': luas_stops,
#         'luas_realtime': luas_realtime,
#     }
#     return render(request, "index/luas.html", context)
