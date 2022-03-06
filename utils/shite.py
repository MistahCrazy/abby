import time
import requests
from random import shuffle
from collections import UserList

class GroundhogDay(UserList):
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.data) - 1: self.i = 0
        self.i += 1
        return self.data[self.i]()
        
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

def crypto_values(currency_code:str = 'BTC') -> dict:
    url = f'https://api.coinbase.com/v2/exchange-rates'

    return get(url, currency=currency_code)['data']

def swap_punc(text: str) -> str:
    return text.replace('.', '|poopie|').replace(',', '.').replace('|poopie|', ',')

# Will all the locale stuff get me into trouble?
def get_bitcoin_usd() -> str:
    value = float(crypto_values('BTC')['rates']['USD'])
    return f'${value:,.2f}'

def get_bitcoin_gpd() -> str:
    value = float(crypto_values('BTC')['rates']['GBP'])
    return f'£{value:,.2f}'

def get_bitcoin_eur() -> str:
    value = float(crypto_values('BTC')['rates']['EUR'])
    return swap_punc(f'{value:,.2f} €')

def get_bitcoin_dkk() -> str:
    value = float(crypto_values('BTC')['rates']['DKK'])
    return swap_punc(f'{value:,.2f}') + ' kr.'

def get_bitcoin_php() -> str:
    value = float(crypto_values('BTC')['rates']['PHP'])
    return f'₱{value:,.2f}'

def get_bitcoin_ars() -> str:
    value = float(crypto_values('BTC')['rates']['ARS'])
    return f'AR${value:,.2f}'

def get_bitcoin_cad() -> str:
    value = float(crypto_values('BTC')['rates']['CAD'])
    return f'CA${value:,.2f}'

def get_bitoin_all() -> dict:
    return {
        'USD': get_bitcoin_usd() + '   ',
        'GPD': get_bitcoin_gpd() + '   ',
        'EUR': get_bitcoin_eur() + ' ',
        'CAD': get_bitcoin_cad() + '   ',
        'DKK': get_bitcoin_dkk(),
        'PHP': get_bitcoin_php() + '   ',
        'ARS': get_bitcoin_ars() + '   '
    }

def get_bitcoin_list() -> GroundhogDay:
    values = GroundhogDay([
        get_bitcoin_usd,
        get_bitcoin_gpd,
        get_bitcoin_eur,
        get_bitcoin_dkk,
        get_bitcoin_php,
        get_bitcoin_ars,
        get_bitcoin_cad
    ])

    shuffle(values)
    return values

if __name__ == '__main__':
    for i in get_bitcoin_list():
       print(i)
       time.sleep(0.25)
