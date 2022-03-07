import time
import requests
from itertools import chain

currencies = {
    'USD': {
        'symbol': '$',
        'suffixed': False,
        'swaped': False,
        'crypto': False
    },
    'GBP': {
        'symbol': '£',
        'suffixed': False,
        'swaped': False,
        'crypto': False
    },
    'EUR': {
        'symbol': '€',
        'suffixed': True,
        'swaped': True,
        'crypto': False
    },
    'DKK': {
        'symbol': 'kr.',
        'suffixed': True,
        'swaped': True,
        'crypto': False
    },
    'PHP': {
        'symbol': '₱',
        'suffixed': False,
        'swaped': False,
        'crypto': False
    },
    'ARS': {
        'symbol': 'AR$',
        'suffixed': False,
        'swaped': False,
        'crypto': False
    },
    'CAD': {
        'symbol': 'CA$',
        'suffixed': False,
        'swaped': False,
        'crypto': False
    },
    'RUB': {
        'symbol': '₽',
        'suffixed': False,
        'swaped': False,
        'crypto': False
    },
    'BTC': {
        'symbol': '₿',
        'suffixed': False,
        'swaped': False,
        'crypto': True
    },
    'LTC': {
        'symbol': 'Ł',
        'suffixed': False,
        'swaped': False,
        'crypto': True
    }
}

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

def swap_punc(text: str) -> str:
    return text.replace('.', '|').replace(',', '.').replace('|', ',')

def get_exchange_rate(currency_from:str = 'BTC', currency_to: str = 'USD') -> str:
    out = ''

    try:
        url = f'https://api.coinbase.com/v2/exchange-rates'
        val = get(url, currency=currency_from)['data']
    except KeyError:
        raise ValueError(f'unknown currency code "{currency_from}"')

    try:
        val = round(float(val['rates'][currency_to]), 2)
        cur = currencies[currency_to]
        out = "${:,.2f}".format(val)
        out = str(out) if not cur['swaped'] else swap_punc(str(out))
        out = cur['symbol'] + out if not cur['suffixed'] else out + ' ' + cur['symbol']
    except KeyError:
        raise ValueError(f'unknown currency code "{currency_to}"')

    return out
