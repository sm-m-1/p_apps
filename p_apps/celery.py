from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from p_apps import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p_apps.settings')

app = Celery('p_apps')
# app = Celery('mysite', broker='pyamqp://guest@localhost//')
# app = Celery('p_apps', broker=os.environ['REDIS_URL'])
app.conf.update(BROKER_URL=os.environ.get('REDIS_URL', ''),
                CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', ''))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

