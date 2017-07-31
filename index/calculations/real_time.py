from index.models import Timetable
from datetime import datetime, timedelta


def timetable(route, direction, minutes, hour, day, mins):
    if day != 'Sunday' and day != 'Saturday':
        day = 'Weekday'
    results = []
    print(route, type(route), direction, type(direction), day, type(day), hour, type(hour))
    minutes, seconds = str(minutes).split('.')
    minutes, seconds = int(minutes), int(seconds[:2])
    hour = str(hour)
    if len(hour) == 1:
        hour = '0' + hour
    for j in [hour]:  # hour-1, hour+1]:
        times = Timetable.objects.filter(route=route, direction=direction, day=day, time__startswith=j)
        print(times)
        for i in times:
            actual_time = datetime.strptime(i.time, '%H:%M:%S')
            print(actual_time)
            arrival = actual_time + timedelta(minutes=minutes, seconds=seconds)
            print(arrival)
            arrival = arrival.replace(microsecond=0)
            results += [arrival]

    min, res = 60, results[0].time()

    for i in results:
        if abs(int(i.strftime('%M')) - int(mins)) < min:
            min = abs(int(i.strftime('%M')) - int(mins))
            res = i.time()

    return res