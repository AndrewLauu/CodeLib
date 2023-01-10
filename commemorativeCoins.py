import copy
import json
import logging
import os
import platform
import sys
import time
import urllib.parse

import requests
import schedule
from colorama import Fore
from lxml import etree
import configparser


def getICBCNews() -> tuple:
    logging.info('Getting icbc news...')

    url = 'https://www.icbc.com.cn/ICBC/纪念币专区/default.htm'
    re = requests.get(url)
    html = etree.HTML(re.content.decode('utf8'))
    # logging.info(f'Response status is {re.status_code}')

    news = html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@data-collecting-param')
    urls = html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@href')

    newUrl = 'https://www.icbc.com.cn'
    newNews = news[0]
    newUrl += urllib.parse.unquote(urls[0])
    logging.info(f'Got latest news 《{colored(newNews[:8])}...》')

    return newNews, newUrl


def getPBCNews() -> tuple:
    logging.info('Getting pbc news...')

    url = 'http://www.pbc.gov.cn/huobijinyinju/147948/147964/22786/index1.html'
    re = requests.post(url)
    html = etree.HTML(re.content.decode('utf8'))
    # logging.info(f'Response status is {re.status_code}')

    news = html.xpath('//font[@class="newslist_style"]/a/@title')
    urls = html.xpath('//font[@class="newslist_style"]/a/@href')

    newNews = news[0]
    newUrl = 'http://www.pbc.gov.cn'
    newUrl += urls[0]
    logging.info(f'Got latest news 《{colored(newNews[:8])}...》')

    return newNews, newUrl


def colored(string: str) -> str:
    return Fore.RED + string + Fore.RESET


def main(msgChannel: set) -> None:
    icbcNews, icbcUrl = getICBCNews()
    pbcNews, pbcUrl = getPBCNews()

    if not os.path.isfile('commemorativeCoins.json'):
        jsonTemp = {
            "icbc": {
                "news": "t",
                "url": "url"
            },
            "pbc": {
                "news": "t",
                "url": "url"
            }
        }
        with open('commemorativeCoins.json', 'w') as f:
            json.dump(jsonTemp, f)
        logging.debug('Did not find json log, created one.')

    with open('commemorativeCoins.json', 'r') as f:
        oldVersion = json.load(f)
    logging.debug('Read json log.')

    newVersion = copy.deepcopy(oldVersion)
    newVersion['icbc']['news'] = icbcNews
    newVersion['icbc']['url'] = icbcUrl
    newVersion['pbc']['news'] = pbcNews
    newVersion['pbc']['url'] = pbcUrl

    if oldVersion != newVersion:
        # send change
        content = [icbcNews, pbcNews]
        url = [icbcUrl, pbcUrl]
        logging.info(f'Found new article {colored(str(content))}')
        msgChannel.add(sendMail)
        for sendMsg in msgChannel:
            try:
                sendMsg('纪念币更新', content, url)
            except:
                logging.warning('failed to send msg: ', exc_info=True)

        with open('commemorativeCoins.json', 'w') as f:
            json.dump(newVersion, f, ensure_ascii=False)

        logging.debug('Wrote to json log.')

    else:
        # send heartbeat
        for sendMsg in msgChannel:
            try:
                sendMsg('Heartbeat', ['plan is running, did not find new article'], ['a'])
            except:
                logging.warning('failed to send msg: ', exc_info=True)
        logging.info(f'did not find new article')


def sendMail(title: str, contents: list, urls: list) -> None:
    import yagmail, configparser
    conf = configparser.ConfigParser()
    conf.read('keyring.ini')
    address = conf['mail']['mail']
    key = conf['mail']['key']
    content = ''

    for url, con in zip(urls, contents):
        content += f'<br><a href="{url}">{con}</a></br>'
    yag = yagmail.SMTP(address, key, host='smtp.qq.com')
    to = address
    yag.send(to=to, subject=title, contents=content)
    logging.debug(f'sent mail {to=} {title=} {content=}')


def showToast(title: str, content: list, *args) -> None:
    from win10toast import ToastNotifier

    toast = ToastNotifier()
    for c in content:
        toast.show_toast(title, msg=c, icon_path=None)
    logging.debug(f'Made toast {title}')


def showNoti(title: str, content: list, urls: list) -> None:
    for c, u in zip(content, urls):
        cmd = f'termux-notification --action "termux-open-url {u}" --content "tap to open {title}" --title {content}'
        os.system(cmd)
    logging.debug(f'Sent notification {title}')


def getEnv() -> set:
    # 1: win 10 toast 2:email 3:android notification
    msgChannelDict = {
        '1': showToast,
        '2': sendMail,
        '3': showNoti
    }
    baseChannel = set(msgChannelDict.keys())
    defaultChannel = '1' if platform.system() == 'Windows' else '2'
    logging.debug(f'{defaultChannel=}')

    NOTIFIER_CHANNEL = set(os.getenv('NOTIFIER_CHANNEL', defaultChannel))
    logging.debug(f'Get system variant NOTIFIER_CHANNEL:{NOTIFIER_CHANNEL}')
    # NOTIFIER_CHANNEL = set(NOTIFIER_CHANNEL)

    if not NOTIFIER_CHANNEL.issubset(baseChannel):
        NOTIFIER_CHANNEL &= baseChannel
        logging.warning(colored(
            f'Only {baseChannel} expected in NOTIFIER_CHANNEL, {NOTIFIER_CHANNEL} was given. Aborted illegal options.'))

    msgChannel = set()

    for i in NOTIFIER_CHANNEL:
        msgChannel.add(msgChannelDict[i])

    logging.info(f'Message sendMsg set as {NOTIFIER_CHANNEL}:{[f.__name__ for f in msgChannel]}')
    return msgChannel


def logPlan():
    plan = [repr(p) for p in schedule.get_jobs('mainPlan')]
    logging.info('\n'.join(plan))


if __name__ == '__main__':
    fileHandler = logging.FileHandler('commemorativeCoins.log')
    fileHandler.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.INFO)

    # init root logger by setting basicConfig
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(module)s.%(funcName)s [%(levelname)s]: %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        handlers=[fileHandler, consoleHandler],
        encoding='utf8'
    )
    logging.info('Started process.')
    # colorama init
    # init(autoreset=True)

    msgChannel = getEnv()

    if len(sys.argv) > 1 and sys.argv[1] == 'asplan':
        schedule.every(4).hours.do(logPlan)
        schedule.every().day.at('10:00').do(main, msgChannel=msgChannel).tag('mainPlan')

        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(10)
    else:
        main(msgChannel=msgChannel)
