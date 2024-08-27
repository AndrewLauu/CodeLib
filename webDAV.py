from webdav3.client import Client
from webdav3.exceptions import RemoteResourceNotFound, ResponseErrorCode, NoConnection
import os,sys,time
# return 0: success
# return 1: other failure
# return 100: webDAV connect fail
# return 101: upload failed
# return 102: given file not found in remote
# return 105: wrong args


def check(file:str|None=None):

    file=os.path.basename(file) if file else ''
    
    try:
        client.list(davBaseDir+'/'+file)
    except RemoteResourceNotFound:
        print(f'[x] check: {file} not fount in webDAV')
        return 102
    except NoConnection:
        print('[x] check: No connection')
        return 100
    if file:
        print(f'[✓] check: {file} exists in webDAV')
    else:
        print('[✓] check: Connected')
    return 0

def upload(file:str):
    if not os.path.isfile(file):
        print('[x] '+file+' not found.')
        return 1
    
    while check()!=0:
        global connRetry
        if connRetry>=maxRetry:
            print(f'[x] Connect fail with {connRetry=}')
            return 100
        time.sleep(1)
        connRetry+=1
        print(f'[!] {connRetry=}')
        upload(file)

    basename=os.path.basename(file)
    print(f'[*] Uploading {basename}...')
    # startTime=time.perf_counter()
    try:
        client.upload(f'{davBaseDir}/{basename}',file)
    except ResponseErrorCode as e:
        msg='The upstream traffic rate is exhausted.'
        if msg.encode() in e.message:
            print('[x] Upload failed. '+msg)
            return 101

    while check(basename)!=0:
        global uploadRetry
        if uploadRetry>=maxRetry:
            print(f'[x] Upload failed with {uploadRetry=}')
            return 101
        time.sleep(1)
        uploadRetry+=1
        print(f'[!] {uploadRetry=}')
        upload(file)
    else:
        # stopTime=time.perf_counter()
        # timeElasped=round(stopTime-startTime,2)
        print(f'[✓] Upload finish')#, time elapsed: {timeElasped}')
        return 0


if __name__=='__main__':
    # print(f'Webdav init with args: {sys.argv}')
    
    # 0: webDAV.py 1: check/upload 2: <file>
    if len(sys.argv)<3:
        print(f'[x] Wrong args: {sys.argv}')
        exit(105)

    mode=sys.argv[1]
    if mode not in ('check','upload'):
        print(f'.[x] Wrong {mode=}')
        exit(105)
    
    file=sys.argv[2:]
    
    # options = {
    #         'webdav_hostname': "https://dav.jianguoyun.com/dav/",
    #         'webdav_login'   : "andrew_lauu@126.com",
    #         'webdav_password': "agznc64g7d2pgyf9"
    #         }
    port:str=os.getenv('ALIDAVPORT') or '13300'
    options = {
            'webdav_hostname': 'http://127.0.0.1:'+port, 
            # 'webdav_login'   : "",
            # 'webdav_password': "",}
            }
    client = Client(options)
    client.webdav.disable_check=True
    # client.verify=False
    davBaseDir='/TERMUX'
    
    maxRetry=2
    uploadRetry=0
    connRetry=0
    exitCode= [0]
    func={
        'check':check,
        'upload':upload
        }[mode]
    
    for f in file:
        retCode=func(f)
        exitCode.append(retCode)
        print(f'[✓] {f}' if retCode==0 else f'[x] {f}')

    exit(max(exitCode))
