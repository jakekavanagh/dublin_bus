import requests
import datetime


"""return the wunderground weather data for the day and time passed through"""
data = requests.get("http://api.wunderground.com/api/37d281e3f1931e1e/hourly10day/q/Ireland/Dublin.json").json()
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday',
            'Wednesday', 'Thursday', 'Friday', 'Saturday']
time = 12
day = "Wednesday"

change = time - int((datetime.datetime.now()).strftime("%H"))
diff = (days[days.index((datetime.datetime.now()).strftime("%A")):].index(day)*24-1)+ change

print(data['hourly_forecast'][diff]['condition'])
