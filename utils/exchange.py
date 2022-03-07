import time
import requests
from functools import partial
from collections import UserList
from collections.abc import Iterable
from itertools import chain

class ExchangeLoop(UserList):
    def __init__(self, iterable: Iterable = [], prefix: str = ''):
        super().__init__(iterable)
        self.prefix = prefix

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.i %= len(self.data)
        value = self.data[self.i]()
        self.i += 1

        return f'{self.prefix} {value}' if self.prefix else value

class throttle(object):
    def __init__(self, seconds):
        self.interval = seconds 
        self.last_time = 0
        self.last_value = {}

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            key = ':'.join(chain(args, kwargs.values()))
            diff = time.time() - self.last_time

            if diff < self.interval and key in self.last_value:
                return self.last_value[key]
                
            self.last_time = time.time()
            self.last_value[key] = fn(*args, **kwargs)

            return fn(*args, **kwargs)

        return wrapper

@throttle(900)
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

def get_exchange_loop(currency_from, prefix: str = '') -> ExchangeLoop:
    return ExchangeLoop([
            partial(get_exchange_usd, currency_from),
            partial(get_exchange_gbp, currency_from),
            partial(get_exchange_eur, currency_from),
            partial(get_exchange_dkk, currency_from),
            partial(get_exchange_php, currency_from),
            partial(get_exchange_ars, currency_from),
            partial(get_exchange_cad, currency_from)
    ], prefix)

if __name__ == '__main__':
    from random import choice

    loops = (
        iter(get_exchange_loop('RUB', '₽ at ')),
        iter(get_exchange_loop('BTC', '₿ at '))
    )

    while True:
       print(next(choice(loops)))
       time.sleep(0.5)
