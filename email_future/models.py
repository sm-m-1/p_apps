from django.db import models
from timezone_field import TimeZoneField
import pytz
from datetime import datetime, timedelta, time

# Create your models here.

def add_gmt_offset_to_choices():
    """
    Currently timezone choices items show up like this:
    'America/New_York'

    But this function formats the choices to display in this format:
    GMT-05:00 America/New_York

    :return:
    A list of tuples in this format:
    (<pytz.timezone>, <str>)
    """
    timezones = pytz.common_timezones_set
    gmt_timezone = pytz.timezone('Greenwich')
    time_ref = datetime(2000,1,1)
    time_zero = gmt_timezone.localize(time_ref)
    _choices = []
    for tz in timezones:
        z = pytz.timezone(tz)
        delta = ( time_zero - z.localize(time_ref) ).total_seconds()
        h = ( datetime.min + timedelta(seconds=delta.__abs__()) ).hour
        gmt_diff = time(h).strftime('%H:%M')
        pair_two = "GMT{sign}{gmt_diff} {timezone}".format(
            sign="-" if delta < 0 else "+",
            gmt_diff=gmt_diff,
            timezone=tz
        )
        pair_one = pytz.timezone(tz)
        _choices.append( (delta, pair_one, pair_two) )

    _choices.sort(key=lambda x: x[0])
    choices = [(one, two) for zero, one, two in _choices]
    return choices


def get_formatted_timezone_set():
    timezones = pytz.common_timezones_set
    timezones = [(t, t) for t in timezones]
    timezones.sort(reverse=True)
    # timezones = [(pytz.timezone(t), t) for t in timezones]
    return timezones[:20]


class UserEmail(models.Model):
    email_subject = models.CharField(null=False, max_length=200)
    email_message = models.TextField(null=False)
    recipient_email = models.EmailField(null=False)
    sender_name = models.CharField(null=False, max_length=100)
    sender_email = models.EmailField(null=False)
    sending_time = models.DateTimeField(null=False)
    sending_timezone = TimeZoneField(
        null=True,
        choices=add_gmt_offset_to_choices()
    )


    def __str__(self):
        return self.email_subject
