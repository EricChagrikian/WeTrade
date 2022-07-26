from optparse import Values
from time import sleep

from requests import request
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen ,Request
from .models import Cryptocurrency


@shared_task
def crawl_currency():
    print('Crwaling data and creating objects in database')
    req = Request ('https://coinranking.com', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    rows = bs.find('tbody', class_= "table__body").find_all('tr', class_= "table__row")[0:10]
    for row in rows:
        cryptocurrency = row.find('span', class_="profile__name").get_text().strip().replace('\n','')
        values = row.find_all('div', class_="valuta")
        price = values[0].get_text().strip().replace('\n','')
        market_cap = values[1].get_text().strip().replace('\n','')
        #change = row.find('div', class_="change").find('span').get_text().strip().replace('\n', '')
        print({'cryptocurrency': cryptocurrency, 'price': price, 'market_cap': market_cap})


        Cryptocurrency.objects.create(
            cryptocurrency=cryptocurrency, 
            price=price, 
            market_cap=market_cap,
            #change=change
        )

        sleep(3)


def update_currency():
    print('Uptating data')
    req = Request ('https://coinranking.com', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    rows = bs.find('tbody', class_= "table__body").find_all('tr', class_= "table__row")[0:10]
    for row in rows:
        cryptocurrency = row.find('span', class_="profile__name").get_text().strip().replace('\n', '')
        values = row.find_all('div', class_="valuta")
        price = values[0].get_text().strip().replace('\n', '')
        market_cap = values[1].get_text().strip().replace('\n', '')
        #change = row.find('div', class_="change").find('span').get_text().strip().replace('\n', '')
        data = {'cryptocurrency': cryptocurrency, 'price': price, 'market_cap': market_cap}
        print({'cryptocurrency': cryptocurrency, 'price': price, 'market_cap': market_cap})
        Cryptocurrency.objects.filter(cryptocurrency=cryptocurrency).update(**data)
        sleep(3)

crawl_currency()
while True:
    update_currency()
    sleep(15)
