import requests
from pprint import pprint
import os
import json
import csv


# routes = ['1', '102', '104', '11', '111', '114', '116', '118', '120', '122', '123', '13', '130', '14', '140',
#                '142', '145', '14C', '15', '150', '151', '15A', '15B', '16', '161', '16C', '17', '17A', '18', '184',
#                '185', '220', '236', '238', '239', '25', '25A', '25B', '25X', '26', '27', '270', '27A', '27B', '27X',
#                '29A', '31', '31B', '32', '32A', '32B', '32X', '33', '33A', '33B', '33X', '37', '38', '38A', '38B', '39',
#                '39A', '4', '40', '40B', '40D', '41', '41A', '41B', '41C', '41X', '42', '43', '44', '44B', '45A', '46A',
#                '46E', '47', '49', '51D', '51X', '53', '54A', '56A', '59', '61', '63', '65', '65B', '66', '66A', '66B',
#                '66X', '67', '67X', '68', '68A', '69', '69X', '7', '70', '747', '75', '76', '76A', '77A', '79', '79A',
#                '7B', '7D', '8', '83', '83A', '84', '84A', '84X', '9']
#
# notfound = ['14C', '15A', '15B', '16C', '17A', '025', '25A', '25B', '25X', '031', '032', '033', '037', '07B', '07D']

# done =['1', '44B', '14', '140', '53', '142', '116', '114', '83', '66B', '16', '151', '236', '69X','41',
#           '65', '32B', '83A', '68', '11', '104', '79','38', '45A', '66A', '18', '43', '42', '41C', '68A', '123',
#           '15', '238', '66X', '79A', '122', '56A', '67X', '67', '27X', '59', '46A', '40', '84A', '747', '47',
#           '41B', '185', '66', '38B', '4', '41A', '33X', '61', '84', '145', '239', '130', '51D', '40D', '29A', '31B',
#           '77A', '161', '32A', '51X', '39A', '32X', '270','17', '130', '239', '84', '33X', '41A', '4', '41B', '66X',
#           '41C', '17',
#           '76A','49', '70', '184', '33A',
#           '84X', '44', '27', '111', ]
# _____________________________________________________________________________________________________________________

# routes = ['13', '7', '102', '76', '118', '40B', '33B', '54A', '65B', '27B', '120', '63',
#           '75', '9', '27A', '8', '46E', '26', '69', '41X', '220', '38A', '150', '39']

routes = ['36A']
schedule_array = []

BusSchedule_csv = open("BusSchedule.csv", 'w', newline='')
write_to = csv.writer(BusSchedule_csv, dialect='excel')
schedule_info = ["Route", "Direction", "Schedule", "Time", "Route_name", "StopID"]
write_to.writerow(schedule_info)

for route_num in routes:
    print("_____________________________________________")
    print("The route number is:", route_num)

    directory = os.fsencode("C:/Users/cindy/Desktop/csv/Cindy")
    route_pad = route_num.zfill(3)

    json_file = open('stops in order.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)

    for direction in json_data[route_pad]:

    # for i in range(0,2):
        print("   --------------------------    ")
        print("Route: ", route_num, "Direction, ", direction)
        print(direction, ":", json_data[route_pad][direction])
        try_this = json_data[route_pad][direction][0]
        print("Is it this one?: ", try_this)
        print("Enter stopID:")
        input_q = input("Enter none for yes, else stopID ")

        if input_q == "":
            input_stop = json_data[route_pad][direction][0]
        else:
            input_stop = input_q

        print("Enter the Route name")
        route_name = input("Route name:::::")

        if route_name == "":
            route_name = input("Try again Route name:::::")

        url = 'https://data.dublinked.ie/cgi-bin/rtpi/timetableinformation?type=week&stopid=' + input_stop + \
              '&routeid=' + str(route_num)

        response = requests.get(url)
        result = response.json()



        # print("Address for Origin!!!")
        # input_origin = input("Origin::::")
        for b in result['results']:
            print("destination: ", b['destination'])
            print("And the times: ", b['departures'])
            print("----------------------------------")

        print("Choose a destination: ")
        for a in result['results']:
            pprint(a['destination'])

        print("Now whats the address of the destination")
        input_dest = input("Destination:::: ")

        if input_dest == "":
            input_dest = input("\nagain Destination:::: ")

        # route_name = str(input_origin + " - " + input_dest)
        print("Route name", route_name)

        for i in result['results']:
            print("\n\n\n")
            print("i['destination']:", i['destination'], ".  input:", input_dest)
            weekday = []
            if str(i['destination']) == input_dest:
                print("Its a match")

                if i['enddayofweek'] == "Friday":
                    print("Weekday!")
                    weekday_raw = i['departures']
                    [weekday.append(item) for item in weekday_raw if item not in weekday]
                    print('Mon_Fri', weekday)

                    for time in weekday:
                        schedule_array = []
                        schedule_array = [route_num, direction, "Weekday", time, route_name, input_stop]
                        print(schedule_array)
                        write_to.writerow(schedule_array)

                elif i['enddayofweek'] == "Saturday":
                    print("Saturday!")
                    saturday_raw = i['departures']
                    saturday = []
                    [saturday.append(item) for item in saturday_raw if item not in saturday]
                    print('Sat', saturday)

                    for time in saturday:
                        schedule_array = [route_num, direction, "Saturday",  time, route_name, input_stop]
                        print(schedule_array)
                        write_to.writerow(schedule_array)

                elif i['enddayofweek'] == "Sunday":
                    print("Sunday!")
                    sunday_raw = i['departures']
                    sunday = []
                    [sunday.append(item) for item in sunday_raw if item not in sunday]
                    print('Sun', sunday)

                    for time in sunday:
                        schedule_array = [route_num, direction, "Sunday", time, route_name, input_stop]
                        print(schedule_array)
                        write_to.writerow(schedule_array)

BusSchedule_csv.close()







# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     if filename.endswith(".json"):
#         with open("C:/Users/cindy/Desktop/csv/Cindy/" + filename) as data_file:
#             data = json.load(data_file)
#         print("\nThe data::::", data['index'])
#         route = filename.rstrip(".json")[0:3].lstrip("0")
#         direction = filename.rstrip(".json").strip()[-1]
#         print(filename, route, direction)