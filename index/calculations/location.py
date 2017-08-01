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
    closest, closest2, closest3, closest4, closest5 = stops[0], stops[1], stops[2], stops[3], stops[4]
    closest_distance = get_distance(float(lat), float(long), float(dicty[stops[0]]['Lat']), float(dicty[stops[0]]['Lon']))
    closest_distance2 = get_distance(float(lat), float(long), float(dicty[stops[1]]['Lat']), float(dicty[stops[1]]['Lon']))
    closest_distance3 = get_distance(float(lat), float(long), float(dicty[stops[2]]['Lat']), float(dicty[stops[2]]['Lon']))
    closest_distance4 = get_distance(float(lat), float(long), float(dicty[stops[3]]['Lat']), float(dicty[stops[3]]['Lon']))
    closest_distance5 = get_distance(float(lat), float(long), float(dicty[stops[4]]['Lat']), float(dicty[stops[4]]['Lon']))
    for stop in stops:
        distance = get_distance(float(lat), float(long), float(dicty[stop]['Lat']), float(dicty[stop]['Lon']))
        if distance < closest_distance:
            closest_distance5, closest_distance4, closest_distance3, closest_distance2, closest_distance = \
                closest_distance4, closest_distance3, closest_distance2, closest_distance, distance
            closest5, closest4, closest3, closest2, closest = closest4, closest3, closest2, closest, stop

        elif distance < closest_distance2:
            closest_distance5, closest_distance4, closest_distance3, closest_distance2 = \
                closest_distance4, closest_distance3, closest_distance2, distance
            closest5, closest4, closest3, closest2 = closest4, closest3, closest2, stop

        elif distance < closest_distance3:
            closest_distance5, closest_distance4, closest_distance3 = closest_distance4, closest_distance3, distance
            closest5, closest4, closest3 = closest4, closest3, stop

        elif distance < closest_distance4:
            closest_distance5, closest_distance4 = closest_distance4, distance
            closest5, closest4 = closest4, stop

        elif distance < closest_distance5:
            closest_distance5 = distance
            closest5 = stop

    return [[closest, dicty[closest]['Lat'], dicty[closest]['Lon']],
            [closest2, dicty[closest2]['Lat'], dicty[closest2]['Lon']],
            [closest3, dicty[closest3]['Lat'], dicty[closest3]['Lon']],
            [closest4, dicty[closest4]['Lat'], dicty[closest4]['Lon']],
            [closest5, dicty[closest5]['Lat'], dicty[closest5]['Lon']]]


def path(stops, dict):
    arr = []
    names = []
    for stop in stops:
        arr += [[dict[stop]['Lat'], dict[stop]['Lon']]]
        names += [str(dict[stop]['name'])]
    return arr, names
