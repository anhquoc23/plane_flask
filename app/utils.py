import hashlib
import hmac
import json
from datetime import datetime
import random as rand



datetime_f = '%Y-%m-%d %H:%M'

def str_datetime(date):
    date = date.replace('%3A', ':')
    date = date.replace('T', ' ')
    return date






if __name__ == '__main__':
    n = str(rand.randint(10 ** 11, 10 ** 12 - 1)) + datetime.now().strftime('%Y%m%d%H%M%S')
    n_str = str(n)
    print(vnpt_payment(int(1270000.0), 'Thanh toán demo', n_str, '127.0.0.1', cb_id=2))