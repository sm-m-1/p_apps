release: python manage.py migrate
web: gunicorn p_apps.wsgi --log-file -
worker: celery -A p_apps2 worker -l info