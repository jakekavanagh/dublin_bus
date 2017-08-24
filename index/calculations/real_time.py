from index.models import Timetable
from datetime import datetime, timedelta


def timetable(route, direction, minutes, hour, day, mins):
    if day != 'Sunday' and day != 'Saturday':
        day = 'Weekday'
    results = []
    previous = []
    if minutes != 0.0:
        minutes, seconds = str(minutes).split('.')
        minutes, seconds = int(minutes), int(seconds[:2])
    else:
        minutes, seconds = 0, 0
    for j in range(int(hour)-1, 24):
        j = str(j)
        if len(j) == 1:
            j = '0' + j
        times = Timetable.objects.filter(route=route, direction=direction, day=day, time__startswith=j)
        for i in times:
            try:
                actual_time = datetime.strptime(i.time, '%H:%M:%S')
            except:
                actual_time = datetime.strptime(i.time, '%H:%M')
            arrival = actual_time + timedelta(minutes=minutes, seconds=seconds)
            arrival = arrival.replace(microsecond=0)
            if int(arrival.strftime('%H')) == int(hour) and int(arrival.strftime('%M')) < int(mins):
                previous += [arrival.time()]
            elif int(arrival.strftime('%H')) >= int(hour):
                results += [arrival.time()]


        if len(results) > 1:
            break
    results.append("No bus available")
    results.append("No bus available")
    previous.insert(0, "No bus available")

    if len(previous) < 2:
        for j in range(int(hour)-1, 6, -1):
            j = str(j)
            if len(j) == 1:
                j = '0' + j
            times = Timetable.objects.filter(route=route, direction=direction, day=day, time__startswith=j)
            for i in times:
                try:
                    actual_time = datetime.strptime(i.time, '%H:%M:%S')
                except:
                    actual_time = datetime.strptime(i.time, '%H:%M')
                arrival = actual_time + timedelta(minutes=minutes, seconds=seconds)
                arrival = arrival.replace(microsecond=0)
                if int(arrival.strftime('%H')) == int(hour) and int(arrival.strftime('%M')) > int(mins):
                    pass
                else:
                    previous += [arrival.time()]
            if len(previous) > 0:
                break

    return results[0], results[1], previous[-1]

