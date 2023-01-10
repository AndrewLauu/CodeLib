import random
import time
from hashlib import sha1
#import hashlib
#otpauth://totp/NeteaseMail:lover_andrew@126.com?secret=****&issuer=NeteaseMail
def gen():
    seed='0123456789abcdefghijklmnopqrstuvwxyz'.upper()
    key=''
    for i in range(16):
        key+=random.choice(seed)
    qr=f'otpauth://totp/Admin?secret={key}&issuer=Filed'
    key=key.encode()
    print('key',key)
    print('qr',qr)
    return qr
def test(key):
    key=key.encode()
    current=time.time()
    timeKey=int(int(current)/30)
    timeKey=str(timeKey).encode()
    print('time',timeKey)
    #sha1=hashlib.sha1()
    secret=key+timeKey
    print(secret)
    #secret=secret.
    auth=sha1(secret).digest()#.encode()
    print(auth)
    auth=sha1(key+auth).hexdigest()
    #auth=sha1.update(secret)
    print(auth)
