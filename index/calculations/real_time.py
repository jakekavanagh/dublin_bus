from index.models import Timetable
from datetime import datetime, timedelta


def timetable(route, direction, minutes, hour, day, mins):
    if day != 'Sunday' and day != 'Saturday':
        day = 'Weekday'
    results = []
    print(route, direction, hour, day)
    minutes, seconds = str(minutes).split('.')
    minutes, seconds = int(minutes), int(seconds[:2])
    for j in [hour]:  # hour-1, hour+1]:
        times = Timetable.objects.filter(route=route, direction=direction, day=day, time__startswith=str(j))
        for i in times:
            actual_time = datetime.strptime(i.time, '%H:%M:%S')
            arrival = actual_time + timedelta(minutes=minutes, seconds=seconds)
            arrival = arrival.replace(microsecond=0)
            results += [arrival]

    min, res = 60, results[0].time()

    for i in results:
        if abs(int(i.strftime('%M')) - int(mins)) < min:
            min = abs(int(i.strftime('%M')) - int(mins))
            res = i.time()

    return res
