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
