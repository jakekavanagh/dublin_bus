from django.db import models
from django.core.urlresolvers import reverse
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    is_student = models.BooleanField(default=False)
    has_leap = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('index:detail', kwargs={'questions_text': self.question_text})

    def __str__(self):
        return self.question_text


class EventApi(models.Model):
    title = models.CharField(max_length=200)
    created = models.BigIntegerField(unique=True)
    start_time = models.BigIntegerField()
    # start_time_readable = models.DateTimeField(default=datetime.datetime.fromtimestamp(start_time).strftime('%m-%d %H:%M'))
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


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
