from django.forms import ModelForm
from django import forms
from email_future.models import UserEmail
from django.utils import timezone
from p_apps import settings
from datetime import datetime, timedelta

class UserEmailorm(ModelForm):
    eta_date = forms.DateField()
    eta_time = forms.TimeField()
    class Meta:
        model = UserEmail
        fields = [
            'email_subject',
            'email_message',
            'recipient_email',
            'sender_name',
            'sender_email',
            # 'sending_time',
            'eta_date',
            'eta_time',
            'sending_timezone'
        ]

    def clean(self):
        data = super().clean()
        # make sure that the date is in the future.
        eta_date = self.cleaned_data.get('eta_date')
        eta_time = self.cleaned_data.get('eta_time')
        sending_timezone = self.cleaned_data.get('sending_timezone') # this is type: pytz.tzfile
        eta_datetime = datetime.combine(eta_date, eta_time)
        eta_input_datetime = sending_timezone.localize(eta_datetime)
        # now_datetime = timezone.now() + timedelta(minutes=5)
        now_datetime = timezone.now()
        # make sure that the use has enterdied a time into the future
        if eta_input_datetime < now_datetime:
            raise forms.ValidationError("You can not select a time in the past!")

        return data