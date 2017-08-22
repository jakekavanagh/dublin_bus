from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
import json
import math

#test the detail page return status,whether it redirects to the http website


class detailTest(TestCase):
    def test_index_view_(self):
        response=self.client.get('/detail')
        self.assertEqual(response.status_code,301)

#test the find page return status,whether it redirects to the http website
class findTest(TestCase):
 def test_mobile_view_(self):
  response = self.client.get('/find')
  self.assertEqual(response.status_code, 301)


#test the luas page return status,whether it redirects to the http website
class luasTest(TestCase):
 def test_mobile_view_(self):
  response = self.client.get('/luas')
  self.assertEqual(response.status_code, 301)


#test the funtion in direct
class routeTest(TestCase):

 def routey(self,route):
  route = str(route)
  if len(route) == 3:
   key = route
  elif len(route) == 2:
   key = '0' + route
  elif len(route) == 1:
   key = '00' + route
  return key
 #test whehter the route would return the right route when query
 def test_routey(self):
  route=self.routey(1)
  self.assertEqual(route, '001')

#test whether the function would work to get the right bus route number
 def bare(self,x):
  while x[0] == '0':
   x = x[1:]
  return x

 def test_bare(self):
  number=self.bare('011')
  self.assertEqual(number,'11')

#test the function in location
class distanceTest(TestCase):

 #test the function whether it would calculate the distance between the given latitude and longitude
 def get_distance(self,lat, long, lat_2, long_2):
   r = 6378137  # Earth’s mean radius in meter
   at=lat_2 - lat
   on=long_2 - long
   d_lat = at* math.pi / 180
   d_long = on* math.pi / 180
   a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(lat* math.pi / 180) * math.cos(lat_2* math.pi / 180) * math.sin(d_long / 2) \
                                                      * math.sin(d_long / 2)
   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
   d = r * c
   return d  # returns the distance in meter
 #give the two latitude and longitude to calculate the distance
 def test_location_distance_(self):
    distance=self.get_distance(53.347012, -6.284541, 53.346756, -6.283194)
    self.assertEqual(distance,93.94074067021972)





#test the function rad
class radTest(TestCase):
 def rad(self,x):
  return x * math.pi / 180
#change to the rad
 def test_rad(self):
  round=self.rad(500)
  self.assertEqual(round,8.726646259971647)




class summaryTest(TestCase):
 def summary_weather(self,condition):
  """convert the summary data code to its corresponding numeric representation"""
  if condition == "Clear":
   return 1
  elif condition == "Fog":
   return 2
  elif condition == "Light Drizzle":
   return 3
  elif condition == "Chance of Rain":
   return 4
  elif condition == "Light Rain Showers":
   return 5
  elif condition == "Light Small Hail Showers":
   return 6
  elif condition == "Light Snow Showers":
   return 7
  elif condition == "Mostly Cloudy":
   return 8
  elif condition == "Overcast":
   return 9
  elif condition == "Partly Cloudy":
   return 10
  elif condition == "Patches of Fog":
   return 11
  elif condition == "Rain":
   return 12
  elif condition == "Scattered Clouds":
   return 13
  elif condition == "Shallow Fog":
   return 14
  elif condition == "Thunderstorm":
   return 15
  else:
   return -1
#test the summary data code to its corresponding numeric representation is work
 def test_summary(self):
  self.assertEqual(self.summary_weather("Rain"),12)
