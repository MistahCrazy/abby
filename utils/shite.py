import time
import requests
from random import shuffle
from collections import UserList
from functools import partial

class GroundhogDay(UserList):
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.i %= len(self.data)
        value = self.data[self.i]()
        self.i += 1

        return value

class to_cache_or_not_to_cache(object):
    def __init__(self, seconds):
        self.interval = seconds 
        self.last_time = 0
        self.last_value = {}

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            diff = time.time() - self.last_time

            if diff < self.interval:
                return self.last_value
                
            self.last_time = time.time()
            self.last_value = fn(*args, **kwargs)

            return self.last_value 

        return wrapper

@to_cache_or_not_to_cache(900)
def get(url, **params):
    http = requests.get(url, params=params)

    if not http.ok:
        raise RuntimeError(f'HTTP status code {http.status_code}')

    return http.json()

def get_exchange_rate(currency_from:str = 'BTC', currency_to: str = 'USD') -> float:
    try:
        url = f'https://api.coinbase.com/v2/exchange-rates'
        res = get(url, currency=currency_from)['data']
    except KeyError:
        raise ValueError(f'unknown currency code "{currency_from}"')

    try:
        return round(float(res['rates'][currency_to]), 2)
    except KeyError:
        raise ValueError(f'unknown currency code "{currency_to}"')

def swap_punc(text: str) -> str:
    return text.replace('.', '|poopie|').replace(',', '.').replace('|poopie|', ',')

def get_exchange_usd(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'USD')
    return f'${value:,.2f}'

def get_exchange_gbp(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'GBP')
    return f'£{value:,.2f}'

def get_exchange_eur(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'EUR')
    return swap_punc(f'{value:,.2f} €')

def get_exchange_dkk(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'DKK')
    return swap_punc(f'{value:,.2f}') + ' kr.'

def get_exchange_php(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'PHP')
    return f'₱{value:,.2f}'

def get_exchange_ars(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'ARS')
    return f'AR${value:,.2f}'

def get_exchange_cad(currency_from) -> str:
    value = get_exchange_rate(currency_from, 'CAD')
    return f'CA${value:,.2f}'

def get_exchanges_btc(currency_from) -> GroundhogDay:
    values = GroundhogDay([
        partial(get_exchange_usd, currency_from),
        partial(get_exchange_gbp, currency_from),
        partial(get_exchange_eur, currency_from),
        partial(get_exchange_dkk, currency_from),
        partial(get_exchange_php, currency_from),
        partial(get_exchange_ars, currency_from),
        partial(get_exchange_cad, currency_from)
    ])
    shuffle(values)

    return values

if __name__ == '__main__':
    for i in get_exchanges_btc('BTC'):
       print(i)
       time.sleep(0.5)
