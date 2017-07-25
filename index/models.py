from django.db import models
from django.core.urlresolvers import reverse
import datetime


class EventApi(models.Model):
    title = models.CharField(max_length=200)
    created = models.BigIntegerField(unique=True)
    start_time = models.BigIntegerField()
    venue_display = models.IntegerField()
    venue_name = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()
    region_name = models.CharField(max_length=200)
    city_name = models.CharField(max_length=200)
    country_name = models.CharField(max_length=200)
    all_day = models.IntegerField()

    def __str__(self):
        return self.title

##make a table that stores all the timetable info

## make a table that stores all the average info
