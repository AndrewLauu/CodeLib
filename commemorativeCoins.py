import requests
from lxml import etree
import urllib.parse
import json
import schedule


def getICBCNews():
    print('getting icbc news')

    url = 'https://www.icbc.com.cn/ICBC/%E7%BA%AA%E5%BF%B5%E5%B8%81%E4%B8%93%E5%8C%BA/default.htm'
    re = requests.get(url)
    html = etree.HTML(re.content.decode('utf8'))

    news = html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@data-collecting-param')
    urls = html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@href')

    newUrl = 'https://www.icbc.com.cn'
    newNews = news[0]
    newUrl += urllib.parse.unquote(urls[0])
    return newNews, newUrl


def getPBCNews():
    print('getting pbc news')

    url = 'http://www.pbc.gov.cn/huobijinyinju/147948/147964/22786/index2.html'
    re = requests.post(url)
    html = etree.HTML(re.content.decode('utf8'))

    news = html.xpath('//font[@class="newslist_style"]/a/@title')
    urls = html.xpath('//font[@class="newslist_style"]/a/@href')

    newNews = news[0]
    newUrl = 'http://www.pbc.gov.cn'
    newUrl += urls[0]

    return newNews, newUrl


def main():
    # 1: toast 2:email
    NOTIFIER_CHANNEL = 1
    if NOTIFIER_CHANNEL == 1:
        sendMsg = sendToast
    else:
        sendMsg = sendMail

    icbcNews, icbcUrl = getICBCNews()
    pbcNews, pbcUrl = getPBCNews()

    with open('commemorativeCoins.json', 'r') as f:
        oldVersion = json.load(f)

    newVersion = oldVersion.copy()
    newVersion['icbc']['news'] = icbcNews
    newVersion['icbc']['url'] = icbcUrl
    newVersion['pbc']['news'] = pbcNews
    newVersion['pbc']['url'] = pbcUrl

    if oldVersion != newVersion:
        # send change
        content = (icbcNews, pbcNews)
        url = (icbcUrl, pbcUrl)

        sendMsg('纪念币更新', content, url)
        with open('commemorativeCoins.json', 'w') as f:
            json.dump(newVersion, f, ensure_ascii=False)
    else:
        # send heartbeat
        sendMsg('heartbeat', ('running',), ('',))


def sendMail(title, contents, urls):
    import yagmail

    content = ''
    for url, con in zip(urls, contents):
        content += f'<a href="{url}">{con}</a>'

    yag = yagmail.SMTP('andrew_lauu@foxmail.com', 'sfrjjkcpkhhsbefa', host='smtp.qq.com')
    yag.send(to='andrew_lauu@126.com', subject=title, contents=content)
    print(f'sent {title}')


def sendToast(title, content, *args):
    from win10toast import ToastNotifier

    toast = ToastNotifier()
    for c in content:
        toast.show_toast(title, c)


if __name__ == '__main__':
    schedule.every().day.at('10:30').do(main)
    while True:
        schedule.run_pending()
