from django.core.mail import send_mail
from p_apps.celery import app

@app.task
def send_mail_wrapper(email_subject, message, from_email, to_email, fail_silently):
    send_mail(email_subject, message, from_email, to_email, fail_silently=fail_silently)