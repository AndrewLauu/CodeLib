# coding=utf-8

import sys
import traceback
import time
import logging
from datetime import date, timedelta
import requests

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By


fileHandler = logging.FileHandler('OaLogin.log', encoding='utf8')
fileHandler.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)

# init root logger by setting basicConfig
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(module)s.%(funcName)s [%(levelname)s]: %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    handlers= [fileHandler, consoleHandler],
    encoding='utf8'
)

# Global logger for this module
logger: logging.Logger = logging.getLogger(__name__)


logger.info('Task begins')


# =========init driver=============
logger.info('Web driver initgating...')

option = FirefoxOptions()
option.set_preference('permissions.default.image', 2)
option.set_preference('permissions.default.stylesheet', 2)
option.add_argument('--headless')

drv = Firefox(options=option)
drv.implicitly_wait(10)

url = 'https://as.boc.cn'
try_count=0

# ========= login =============
def login():
    logger.info(f'Goto {url}')
    drv.get(url)

    logger.info(f'login @{drv.current_url}...')

    drv.find_element(by=By.ID, value="XM").send_keys('刘朋飞')
    drv.find_element(by=By.ID, value='SFZH').send_keys('37028119970702051X')
    drv.find_element(by=By.ID, value='Password').send_keys('Boc123456.')

    drv.find_element(by=By.CLASS_NAME, value='button1').click()

    logger.info(f'wait for login result...')
    
    try:
        drv.switch_to.default_content()
        drv.switch_to.frame("top0")
        drv.find_element(by=By.ID, value='systemName')
    except NoSuchElementException:
        try_count+=1
        logger.warning(f'retry {try_count}')
        if try_count>5:
            raise
        time.sleep(2)
        login()
        
login()
# ========= get balance =============
drv.switch_to.default_content()
drv.switch_to.frame("top0")
title=drv.find_element(by=By.ID, value='systemName')
logger.debug(f'logged in to {title}')

drv.switch_to.default_content()
drv.switch_to.frame("main0")
css_path='#main0 > form tbody > tr:nth-child(2) > td div.div1_2 > table tr:nth-child(1) > td:nth-child(2)'
amount=drv.find_element(by=By.CSS_SELECTOR, value=css_path).text.strip().replace("元", "")
amount=float(amount)


with open("EA.txt","w+") as f:
    amount_old=float(f.read() or 0)
    if abs(amount_old - amount) > 0.01:
        f.write(str(amount))

# ========= get saving =============
drv.switch_to.default_content()
drv.switch_to.frame("top1")
drv.find_element(by=By.ID, value='M0113').click()


EOLM=date.today().replace(day=1) - timedelta(days=-1)
BOLM=EOLM.replace(day=1)
logger.info(f'{BOLM} - {EOLM}')

drv.switch_to.default_content()
drv.switch_to.frame("main0")
drv.find_element(by=By.ID, value='QSSJ').send_keys(BOLM.strftime("%Y%m%d"))
drv.find_element(by=By.ID, value='JZSJ').send_keys(EOLM.strftime("%Y%m%d"))
drv.find_element(by=By.ID, value='chx').click()

drv.switch_to.frame("data")
pay_amount=drv.find_element(by=By.CSS_SELECTOR, value="#tablesorter > tbody > tr:nth-last-of-type(1) > td:nth-of-type(8) strong").text.strip()
pay_amount=float(pay_amount or 0)

desp=f"年金余额{amount}，缴存{pay_amount}，变动{amount-pay_amount-amount_old}"

requests.get(f"https://sctapi.ftqq.com/SCT221971Tw3HrlNQhM2jQ2Xc0C3JWppDo.send?title=年金更新&desp={desp}")
logger.info(desp)

# ========= log out =============
logger.info('finish')
drv.quit()
