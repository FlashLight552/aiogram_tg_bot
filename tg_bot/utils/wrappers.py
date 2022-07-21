from datetime import datetime
from unittest import result

def log(func):
    def wrapper(*args):
        result = func(*args)
        print (f'{datetime.now()}, cmd: {result.__name__}')
        return result     
    return wrapper