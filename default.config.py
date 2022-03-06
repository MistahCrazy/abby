from pathlib import Path

class Client(object):
    prefix = ''
    description = ''
    token = ''
    
    message_limit = 2000
    safe_message_limit = 1936
    upload_limit = 8000000
    error_timeout = 300
    command_timeout = 60

class Paths(tuple):
    base = Path(__file__).parent.resolve()
    data = base / 'data'
    settings = data / 'settings.db'
    chan4 = data / 'chan4.db'
    