from django.db import models
from django.core.urlresolvers import reverse
import datetime


class Event(models.Model):
    event_date = models.CharField(max_length=200)
    weekday = models.CharField(max_length=200)
    event_time = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        unique_together = ('event_date', 'title', 'venue_name', 'event_time')
# make a table that stores all the timetable info

# make a table that stores all the average info


class Averages(models.Model):
    route = models.CharField(max_length=200)
    direction = models.IntegerField()
    stop = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    average = models.FloatField()
    at_stop = models.FloatField()


class RoughAverages(models.Model):
    route = models.CharField(max_length=200)
    direction = models.IntegerField()
    stop = models.IntegerField()
    average = models.FloatField()
    at_stop = models.FloatField()


class Timetable(models.Model):
    route = models.CharField(max_length=200)
    direction = models.IntegerField()
    day = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    destination = models.CharField(max_length=300)
    start_stop = models.IntegerField()


class Twitter(models.Model):
    tweet = models.CharField(max_length=200)
    tweet_date = models.CharField(max_length=200)
    tweet_time = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        unique_together = ('tweet', 'tweet_date', 'tweet_time')


class Luas(models.Model):
    line = models.CharField(max_length=200)
    stop_name = models.CharField(max_length=200)
    stop_id = models.CharField(max_length=200)
    stop_lat = models.FloatField()
    stop_lon = models.CharField(max_length=200)


class RealTime_Luas(models.Model):
    stop_id = models.CharField(max_length=200)
    luas_date = models.CharField(max_length=200)
    luas_time = models.CharField(max_length=200)
    line = models.CharField(max_length=200)
    duetime = models.CharField(max_length=200)
    direction = models.CharField(max_length=200)

