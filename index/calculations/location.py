import math


def rad(x):
    return x * math.pi / 180


def get_distance(lat, long, lat_2, long_2):
    r = 6378137  # Earth’s mean radius in meter
    d_lat = rad(lat_2 - lat)
    d_long = rad(long_2 - long)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(rad(lat)) * math.cos(rad(lat_2)) * math.sin(d_long / 2)\
        * math.sin(d_long / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c
    return d  # returns the distance in meter


def nearest(lat, long, dicty):
    stops = [x for x in dicty]
    closest, closest2, closest3 = stops[0], stops[1], stops[2]
    closest_distance = get_distance(float(lat), float(long), float(dicty[stops[0]]['Lat']), float(dicty[stops[0]]['Lon']))
    closest_distance2 = get_distance(float(lat), float(long), float(dicty[stops[1]]['Lat']), float(dicty[stops[1]]['Lon']))
    closest_distance3 = get_distance(float(lat), float(long), float(dicty[stops[2]]['Lat']), float(dicty[stops[2]]['Lon']))
    for stop in stops:
        distance = get_distance(float(lat), float(long), float(dicty[stop]['Lat']), float(dicty[stop]['Lon']))
        if distance < closest_distance:
            closest_distance3, closest_distance2, closest_distance = closest_distance2, closest_distance, distance
            closest3, closest2, closest = closest2, closest, stop
        elif distance <closest_distance2:
            closest_distance3, closest_distance2 = closest_distance2, distance
            closest3, closest2 = closest2, stop
        elif distance < closest_distance3:
            closest_distance3 = distance
            closest3 = stop

    return [[closest, dicty[closest]['Lat'], dicty[closest]['Lon']], [closest2, dicty[closest2]['Lat'], dicty[closest2]['Lon']],\
           [closest3, dicty[closest3]['Lat'], dicty[closest3]['Lon']]]

