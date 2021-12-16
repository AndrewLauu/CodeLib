import logging
import os
import time

import requests
from lxml import etree
import urllib.parse
import json
import schedule


def getICBCNews():
    logging.debug('Getting icbc news...')

    url = 'https://www.icbc.com.cn/ICBC/纪念币专区/default.htm'
    re = requests.get(url)
    html = etree.HTML(re.content.decode('utf8'))
    logging.info(f'Response status is {re.status_code}')

    news = html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@data-collecting-param')
    urls = html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@href')

    newUrl = 'https://www.icbc.com.cn'
    newNews = news[0]
    newUrl += urllib.parse.unquote(urls[0])
    logging.info(f'Got latest news 《{newNews[:8]}...》')

    return newNews, newUrl


def getPBCNews():
    logging.debug('Getting pbc news...')

    url = 'http://www.pbc.gov.cn/huobijinyinju/147948/147964/22786/index2.html'
    re = requests.post(url)
    html = etree.HTML(re.content.decode('utf8'))
    logging.info(f'Response status is {re.status_code}')

    news = html.xpath('//font[@class="newslist_style"]/a/@title')
    urls = html.xpath('//font[@class="newslist_style"]/a/@href')

    newNews = news[0]
    newUrl = 'http://www.pbc.gov.cn'
    newUrl += urls[0]
    logging.info(f'Got latest news 《{newNews[:8]}...》')

    return newNews, newUrl


def main(msgChannel):

    icbcNews, icbcUrl = getICBCNews()
    pbcNews, pbcUrl = getPBCNews()

    if not os.path.isfile('commemorativeCoins.json'):
        open('commemorativeCoins.json', 'w').close()
        logging.info('Did not find json log, created one.')

    with open('commemorativeCoins.json', 'r') as f:
        oldVersion = json.load(f)
    logging.debug('Read json log.')

    newVersion = oldVersion.copy()
    newVersion['icbc']['news'] = icbcNews
    newVersion['icbc']['url'] = icbcUrl
    newVersion['pbc']['news'] = pbcNews
    newVersion['pbc']['url'] = pbcUrl

    if oldVersion != newVersion:
        # send change
        content = (icbcNews, pbcNews)
        url = (icbcUrl, pbcUrl)
        logging.info(f'Found new article {content}')

        for sendMsg in msgChannel:
            sendMsg('纪念币更新', content, url)

        with open('commemorativeCoins.json', 'w') as f:
            json.dump(newVersion, f, ensure_ascii=False)

        logging.info('Wrote to json log.')

    else:
        # send heartbeat
        for sendMsg in msgChannel:
            sendMsg('Heartbeat', ('plan is running, did not find new article',), ('a',))
        logging.info(f'did not find new article')


def sendMail(title, contents, urls):
    import yagmail

    content = ''
    
    for url, con in zip(urls, contents):
        content += f'<a href="{url}">{con}</a>'
    yag = yagmail.SMTP('andrew_lauu@foxmail.com', 'sfrjjkcpkhhsbefa', host='smtp.qq.com')
    yag.send(to='andrew_lauu@126.com', subject=title, contents=content)
    logging.info(f'sent mail {title}')


def showToast(title, content, *args):
    from win10toast import ToastNotifier

    toast = ToastNotifier()
    for c in content:
        toast.show_toast(title, c)
    logging.info(f'Made toast {title}')

def showNotification(title,content,urls):
    for c,u in zip(content,urls):
        cmd=f'termux-notification --action "termux-open-url {u}" -c "tap to open {title} --title {content}'
        os.system(cmd)
    logging.info(f'Sent notification {title}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: <%(funcName)s> - %(message)s',
                        datefmt='%Y-%d-%m %H:%M:%S')
    logging.debug('Started process.')
    
    # 1: win 10 toast 2:email 3:android notification
    # todo multi way
    if NOTIFIER_CHANNEL:=os.getenv('NOTIFIER_CHANNEL'):
        logging.debug(f'Get system variant NOTIFIER_CHANNEL:{NOTIFIER_CHANNEL}')
        NOTIFIER_CHANNEL=set(NOTIFIER_CHANNEL)
    else:
        NOTIFIER_CHANNEL={'1'}
        logging.debug(f'Use default NOTIFIER_CHANNEL:{NOTIFIER_CHANNEL}')

    baseChannel=set('123')

    if not NOTIFIER_CHANNEL.issubset(baseChannel):
        NOTIFIER_CHANNEL &= baseChannel
        logging.warning(f'Only "1" "2" or "3" expected in NOTIFIER_CHANNEL, {NOTIFIER_CHANNEL} was given. Aborted illegal options.')

    msgChannelDict={
            '1':showToast,
            '2':sendMail,
            '3':showNotification
            }

    msgChannel=[]
    
    for i in NOTIFIER_CHANNEL:
        msgChannel.append(msgChannelDict[i])

    logging.info(f'Message sendMsg set as {NOTIFIER_CHANNEL}:{[f.__name__ for f in msgChannel]}')

    schedule.every().day.at('10:00').do(main,msgChannel=msgChannel)
    logging.debug('Scheduled plan.')
    while True:
        plan = [repr(p) for p in schedule.get_jobs()]
        logging.info(''.join(plan))
        schedule.run_pending()
        time.sleep(60*60*2)
