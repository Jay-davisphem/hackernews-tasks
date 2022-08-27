web: gunicorn newsproject.wsgi --log-file -
worker: celery -A newsapp worker -l info
beat: celery -A newsapp beat -l info
