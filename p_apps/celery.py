from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from p_apps import settings

# BROKER_POOL_LIMIT = 1

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p_apps.settings')

app = Celery('p_apps')

app.conf.update(
    # CELERY_ACCEPT_CONTENT = ['json'],
    # CELERY_TASK_SERIALIZER = 'json',
    # CELERY_RESULT_SERIALIZER = 'json',
    broker_url = os.environ.get('CLOUDAMQP_URL', 'pyamqp://guest@localhost//'),
    broker_pool_limit = 1, # Will decrease connection usage
    broker_heartbeat = None, # We're using TCP keep-alive instead
    broker_connection_timeout = 30, # May require a long timeout due to Linux DNS timeouts etc
    # result_backend = 'django-cache', # AMQP is not recommended as result backend as it creates thousands of queues
    result_backend='rpc', # AMQP is not recommended as result backend as it creates thousands of queues
    event_queue_expires = 60, # Will delete all celeryev. queues without consumers after 1 minute.
    worker_prefetch_multiplier = 1, # Disable prefetching, it's causes problems and doesn't help performance
    worker_concurrency = 50,
)
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

