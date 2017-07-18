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
    closest = stops[0]
    closest_distance = get_distance(float(lat), float(long), float(dicty[stops[0]]['Lat']), float(dicty[stops[0]]['Lon']))
    for stop in stops:
        distance = get_distance(float(lat), float(long), float(dicty[stop]['Lat']), float(dicty[stop]['Lon']))
        if distance < closest_distance:
            closest_distance = distance
            closest = stop
    return [closest, dicty[closest]['Lat'], dicty[closest]['Lon']]

