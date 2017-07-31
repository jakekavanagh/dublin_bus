import csv
from datetime import datetime
from datetime import timedelta


date_time = datetime.strptime("13:00:00", "%H:%M:%S")

BusSchedule_csv = open("BusSchedule145mini2.csv", 'w', newline='')
write_to = csv.writer(BusSchedule_csv, dialect='excel')


for i in range(0, 48):
    add_on = timedelta(minutes=10)
    date_time = date_time + add_on

    info = ['145', '0', 'Weekday', date_time.time(), 'Heuston Rail Station To Ballywaltrim', '4320']
    write_to.writerow(info)


for i in range(0, 6):
    add_on = timedelta(minutes=20)
    date_time = date_time + add_on

    info = ['145', '0', 'Weekday', date_time.time(), 'Heuston Rail Station To Ballywaltrim', '4320']
    write_to.writerow(info)


BusSchedule_csv.close()

















# import requests
# from pprint import pprint
#
#
#
#
# route_id = str(25)
# stopid = str(3890)
#
# url = 'https://data.dublinked.ie/cgi-bin/rtpi/timetableinformation?type=week&stopid=' + stopid +\
#       '&routeid=' + route_id
#
# response = requests.get(url)
# result = response.json()
#
# for i in result['results']:
#     if i['destination'] == 'Dodsboro Rd':
#         if i['enddayofweek'] == "Sunday":
#             print('Sun', i['departures'])
#         elif i['enddayofweek'] == "Friday":
#             print('Mon_Fri', i['departures'])
#         elif i['enddayofweek'] == "Saturday":
#             print('Sat', i['departures'])
