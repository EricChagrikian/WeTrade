from time import sleep
from celery import shared_task
from urllib.request import urlopen
from .models import cryptocurrency


@shared_task
def crawl_currency():
    print('Crwaling data and creating objects in database')
    req = ('https://coin')