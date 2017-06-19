import requests

# ____________________________ Real Time Bus Information __________________________ #
# See Document section 3.4.1

# Change value of Stop Id for a different stop info
stopid = str(1304)

url = 'https://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid=' + stopid
# extra parameters that can be added to the url
# +'&routeid=[routeid]&maxresults&operator=[operator]&format=[format]'

# Establish a connection and retrieve the request
response = requests.get(url)

# Jsonify the result
result = response.json()

stop_id = result['stopid']
time_stamp = result['timestamp']
# arrival_datetime = result['results']['arrivaldatetime']

# display Results
# print("Real Time Stop Information: ", result, '\n\n', "real time info: \n\n")
# for info in result['results']:
#     print(info, '\n')

# _____________________ Timetable Bus Information By Date ____________________ #
# See Document section 3.4.2

stopid = str(1304)
url = 'https://data.dublinked.ie/cgi-bin/rtpi/timetableinformation?type=day&stopid=' + stopid
# extra parameters that can be added to the url
# +'&routeid=[routeid]&datetime=[Date time]&maxresults=[maxresults]&operator=[operator]&format=[format]'

response = requests.get(url)
result = response.json()

# print(result)

# _____________________Full Timetable Bus Information ________________________ #
# See Document section 3.4.3

route_id = str(17)

url = 'https://data.dublinked.ie/cgi-bin/rtpi/timetableinformation?type=week&stopid=' + stopid \
      + '&routeid=' + route_id

response = requests.get(url)
result = response.json()

# print(result)

# _________________________ Bus Stop Information ______________________________ #
# See Document section 3.4.4

url = 'https://data.dublinked.ie/cgi-bin/rtpi/busstopinformation?'

# optional parameters
# 'stopid=' + stopid +'stopname=[stopname]&format=[format]'

response = requests.get(url)
result = response.json()

# print(result)

# __________________________ Route Information ______________________________ #
# See Document section 3.4.5

# required parameters
route_id = str(17)
operator_id = "bac"

url = 'https://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid=' + route_id \
      + '&operator=' + operator_id

response = requests.get(url)
result = response.json()

# print(result)
# for i in result['results']:
    # print(i)

# __________________________ Operator Information ______________________________ #
# See Document section 3.4.6

url = 'https://data.dublinked.ie/cgi-bin/rtpi/operatorinformation?'
response = requests.get(url)
result = response.json()

# print(result, '\n')
# for i in result['results']:
    # print(i)

# __________________________ Route List Information ____________________________ #
# See Document section 3.4.7

url = 'https://data.dublinked.ie/cgi-bin/rtpi/routelistinformation?'
response = requests.get(url)
result = response.json()

print(result)
