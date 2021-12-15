import requests
from lxml import etree
import urllib.parse
import json
import yagmail
import schedule

def getNews():
    print('getting news')
    icbc_url='https://www.icbc.com.cn/ICBC/%E7%BA%AA%E5%BF%B5%E5%B8%81%E4%B8%93%E5%8C%BA/default.htm'


    icbc_re=requests.get(icbc_url)

    icbc_html=etree.HTML(icbc_re.content.decode('utf8'))

    news=icbc_html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@data-collecting-param')
    urls=icbc_html.xpath('//span[@class="ChannelSummaryList-insty"]/a/@href')

    newUrl='https://www.icbc.com.cn'
    newTitle=news[0]
    newUrl+=urllib.parse.unquote(urls[0])

    with open('icbc.json','r') as f:
        oldVersion=json.load(f)

    if oldVersion[0]!=newTitle:
        content=f'<a href="{newUrl}">{newTitle}</a>'
        sendMail(newTitle,content)
        with open('icbc.json','w') as f:
            json.dump([newTitle,newUrl],f,ensure_ascii=False)


def sendMail(sub,cont):
    yag=yagmail.SMTP('andrew_lauu@foxmail.com','sfrjjkcpkhhsbefa',host='smtp.qq.com')
    yag.send(to='andrew_lauu@126.com',subject=sub,contents=cont)
    print(f'sent {sub}')

schedule.every().day.at('09:00').do(sendMail,sub='icbc heartbeat',cont='running')
schedule.every().day.at('10:00').do(getNews)

while True:
    schedule.run_pending()



