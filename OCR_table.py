import requests
import base64
from urllib import parse
import itchat
import time


@itchat.msg_register(itchat.content.PICTURE)
def get_pic(msg):
    # print("Got a pic")
    sender = msg.user.remarkName
    if sender == 'Andrew':
        print('Authorized, encoding...')
        msg.text(msg.fileName)
        with open(msg.fileName, 'rb') as f:
            pic = f.read()
        encode_pic(pic)


def encode_pic(picture):
    pic_64 = base64.b64encode(picture)
    print('Encoded, OCRing...')
    ocr(pic_64, get_access())


def get_access():
    AK = '5V6DrLiK5O2eudgQrWjAilXP'
    SK = 'bwP9UZ1hcuT9lZwGTGTcu9nYOEDBg0jX'
    # APPID = '15631258'
    access_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'client_id': AK,
            'client_secret': SK
            }
    ACK = requests.post(access_url, data=data, headers=header).json()['access_token']
    print('Regenerated access_key.')
    # quit(12)
    return ACK


def ocr(pic_url, ACK):
    post_url = f'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'access_token': ACK,
        'image': pic_url
    }
    data = parse.urlencode(data)
    re = requests.post(post_url, headers=headers, data=data)
    result = re.json()
    print('Posted image.')
    if 'result' in result:
        request_id = result['result'][0]['request_id']
        print(f'Request_id: {request_id}, getting result...')
        status = 1
        file = ''
        ct = 0
        while status != 3:
            status, file, percent = get_result(request_id, ACK)
            print(f'Did not finish, {percent},{ct}')
            ct += 1
            time.sleep(1)
        file_url=file['file_url']
        print(file_url)
    else:
        print('Post error', result['error_code'], result['error_msg'])
        quit()


def get_result(request_id, ACK):
    url = f'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'request_id': request_id,
            'access_token': ACK
            }
    data = parse.urlencode(data)
    result = requests.post(url, headers=headers, data=data).json()
    # print(result)
    percent = ''
    if 'error_code' in result:
        print('Get error', result['error_code'], result['error_msg'])
        status = -1
        file = ''
    else:
        result = result['result']
        status = result['ret_code']
        file = result['result_data']
        percent = result['percent']

    return status, file, percent


if __name__ == '__main__':
    access_key = get_access()
    itchat.auto_login(hotReload=True)
    itchat.run()
