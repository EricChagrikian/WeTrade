web: gunicorn --pythonpath WeTrade ProjectMain.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
python3 manage.py migrate