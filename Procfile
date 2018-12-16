release: python manage.py migrate
web: gunicorn p_apps.wsgi --log-file -
worker: celery -A p_apps worker --beat -l info --app=p_apps.celery