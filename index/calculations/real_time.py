from index.models import Timetable
from datetime import datetime, timedelta


def timetable(route, direction, minutes, hour, day, mins):
    if day != 'Sunday' and day != 'Saturday':
        day = 'Weekday'
    print("\t\t\t", route, day)
    results = []
    previous = []
    if minutes != 0.0:
        minutes, seconds = str(minutes).split('.')
        minutes, seconds = int(minutes), int(seconds[:2])
    else:
        minutes, seconds = 0, 0
    for j in range(int(hour), 24):
        j = str(j)
        if len(j) == 1:
            j = '0' + j
        times = Timetable.objects.filter(route=route, direction=direction, day=day, time__startswith=j)
        print(j, times)
        for i in times:
            try:
                actual_time = datetime.strptime(i.time, '%H:%M:%S')
            except:
                actual_time = datetime.strptime(i.time, '%H:%M')
            arrival = actual_time + timedelta(minutes=minutes, seconds=seconds)
            arrival = arrival.replace(microsecond=0)
            if int(arrival.strftime('%H')) == int(hour) and int(arrival.strftime('%M')) < int(mins):
                previous += [arrival]
            else:
                results += [arrival]
        if len(results) > 1:
            break
    results.append(0)
    results.append(0)

    if len(previous) < 1:
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
                    previous += [arrival]
            if len(previous) >0:
                break

    return results[0].time(), results[1].time(), previous[-1].time()

    # if len(results) > 1:
    #     min, res = abs(int(results[0].strftime('%M')) - int(mins)), results[0].time()
    #     min2, res2 = abs(int(results[1].strftime('%M')) - int(mins)), results[1].time()
    #     for i in results:
    #         if abs(int(i.strftime('%M')) - int(mins)) < min:
    #             min2, min = min, abs(int(i.strftime('%M')) - int(mins))
    #             res2, res = res, i.time()
    #         elif abs(int(i.strftime('%M')) - int(mins)) < min2:
    #             min2 = abs(int(i.strftime('%M')) - int(mins))
    #             res2 = i.time()
    #     print(res, res2)
    #     return str(res), str(res2), 0
    # elif len(results) > 0:
    #     min, res = abs(int(results[0].strftime('%M')) - int(mins)), results[0].time()
    #     for i in results:
    #         if abs(int(i.strftime('%M')) - int(mins)) < min:
    #             min = abs(int(i.strftime('%M')) - int(mins))
    #             res = i.time()
    #
    #     return res, 0, 0
    #
    # else:
    #     return '00.00.00', 0, 0
