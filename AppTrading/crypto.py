from requests import Request, Session
import json
import time
import webbrowser
import pprint

def getInfo (symbol): 

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' # Coinmarketcap API url

    parameters = { 'symbol': symbol , 'convert': 'USD' } 

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ae9c906b-ddb1-4894-85b1-3a8bbc8d8d55'
    } 

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    info = json.loads(response.text)['data'][symbol]['quote']['USD']['price']

    return info
        
