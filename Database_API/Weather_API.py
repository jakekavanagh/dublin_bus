import requests
import datetime
import json


def grab_data(dataa, day):
    """This function takes json input from the response and appends to a
    dictionary with new key and values"""
    a = Weather[day][(i['FCTTIME']['hour'])]
    a['epoch_time'] = i['FCTTIME']['epoch']
    a['time'] = i['FCTTIME']['civil']
    a['month'] = i['FCTTIME']['month_name']
    a['date'] = i['FCTTIME']['mday']
    a['chance_rain'] = i["pop"]
    if float(i["pop"]) >= 50:
        a["rain"] = "1"
    else:
        a["rain"] = "0"
    a["icon"] = i["icon"]
    a["condition"] = i["condition"]
    a["temp"] = i["temp"]["metric"]
    a["wind"] = i["wspd"]["metric"]


def view_dict(dict_name):
    """This function prints the entire dictionary"""
    for keys, values in dict_name.items():
        print(keys, values)


def to_JSON(dict_name):
    """Creates a JSON file with a inputted dictionary"""
    with open('Weather.json', 'w') as fp:
        json.dump(dict_name, fp)


# Url for connecting to the API with search refined to Dublin
url = "http://api.wunderground.com/api/37d281e3f1931e1e/hourly10day/q/Ireland/Dublin.json"
# Parsing the data to JSON format
data = requests.get(url).json()

# Creating new dictionary called Weather to store a subset of the returned data
Weather = {}
weekday_list = []
check = False

# Store the weekday name of today
today = (datetime.datetime.now()).strftime("%A")

# Iterates through the data setting the first day returned to Today, then iteratively
# only keeps 1 week of data thereon after. So if today is friday, the code will
# return until next friday, storing this friday as "Today" and next friday as "Friday"

for i in data['hourly_forecast']:
    weekday = i['FCTTIME']['weekday_name']
    if weekday == today and check is False:
        if "Today" not in weekday_list:
            Weather['Today'] = {}
            Weather['Today'][(i['FCTTIME']['hour'])] = {}
            grab_data(data, "Today")
        else:
            weekday_list.append("Today")
            Weather['Today'][(i['FCTTIME']['hour'])] = {}
            grab_data(data, weekday)
        weekday_list.append("Today")
    else:
        check = True
        while (weekday_list.count(weekday)) <= 24:
            if weekday not in weekday_list:
                weekday_list.append(weekday)
                Weather[weekday] = {}
                Weather[weekday][(i['FCTTIME']['hour'])] = {}
                grab_data(data, weekday)
            else:
                weekday_list.append(weekday)
                Weather[weekday][(i['FCTTIME']['hour'])] = {}
                grab_data(data, weekday)
                break

to_JSON(Weather)