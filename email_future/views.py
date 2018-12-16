from django.core.mail import send_mail
from datetime import datetime

from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from p_apps import settings
from .forms import UserEmailorm
from .tasks import send_mail_wrapper


class EmailAppFormView(generic.FormView):
    template_name = 'email_form.html'
    form_class = UserEmailorm
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        # form = self.get_form()
        # data = form.data
        # print("data: ", data)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # this method is called when valid form data as been posted.
        valid = super().form_valid(form)
        email_subject = form.cleaned_data.get('email_subject')
        email_message = form.cleaned_data.get('email_message')
        recipient_email = form.cleaned_data.get('recipient_email')
        sender_name = form.cleaned_data.get('sender_name')
        sender_email = form.cleaned_data.get('sender_email')
        eta_date = form.cleaned_data.get('eta_date')
        eta_time = form.cleaned_data.get('eta_time')
        sending_timezone = form.cleaned_data.get('sending_timezone')
        print("sending_timezone: ", sending_timezone)
        eta_input_datetime = form.cleaned_data.get('eta_input_datetime')
        message = render_to_string('email.html', {
            'email_message': email_message,
            'sender_name': sender_name,
            'sender_email': sender_email,
        })
        # print("message: ", message)

        print("eta_input_datetime: ", eta_input_datetime)
        send_mail_wrapper.apply_async(
            (
            email_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            False
            ),
            eta=eta_input_datetime
        )
        # send_mail_wrapper.delay(
        #     email_subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [recipient_email],
        #     False
        # )
        # send_mail(
        #     email_subject,
        #     message,settings.DEFAULT_FROM_EMAIL,
        #     [recipient_email],
        #     False
        # )

        return valid

    def get_success_url(self):
        return reverse('email_form_success')

def email_form_success(request):
    return render(request, template_name='email_form_success.html')