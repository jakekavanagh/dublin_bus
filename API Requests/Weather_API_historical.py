import requests
import csv
import math


def weather_scraper(year, month, day):
    # Take date as input
    date = year + month + day

    urlstart = 'http://api.wunderground.com/api/37d281e3f1931e1e/history_'
    urlend = '/q/Ireland/Dublin.json'
    url = urlstart + str(date) + urlend
    data = requests.get(url).json()

    for i in data['history']['observations']:
        # weather_array = []
        if 'METAR' in i['metar']:
            # if i['date']['min'] == "00":
            datetime = year + "-" + month + "-" + day + " " + \
                       i['date']['hour'] + ':' + i['date']['min'] + ':00'
            # print("Time:", datetime)
            summary = i['conds']
            # print(summary)
            temp = str(math.floor(float(i["tempm"])))
            # print("Temp: ", temp)
            rain = i['rain']
            # print("rain: ", rain)
            wind_speed = str(math.floor(float(i['wspdm'])))
            # print("wind speed: ", wind_speed)
            weather_array = [datetime, summary, temp, rain, wind_speed]
            # print(weather_array)

            write_to.writerow(weather_array)


weather_csv = open("weather_csv_halfhourly.csv", 'w', newline='')
write_to = csv.writer(weather_csv, dialect='excel')
weather_info = ["DateTime", "Summary", "Temp", "Rain", "Wind_Speed"]
write_to.writerow(weather_info)

nov_days = ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
            "24", "25", "26", "27", "28", "29", "30"]
jan_days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18",
            "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]

for j in nov_days:
    year = "2012"
    month = "11"
    day = j
    weather_scraper(year, month, day)

for k in jan_days:
    year = "2013"
    month = "01"
    day = k
    weather_scraper(year, month, day)

weather_csv.close()
