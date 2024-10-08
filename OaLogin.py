# coding=utf-8
from random import randint

import sys
import traceback
import time
import logging

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as Wait
# from selenium.webdriver.common.keys import Keys
import sys
import datetime
import traceback
import logging


# =========error handler=============
def callback_func(exc_type, exc_value, exc_traceback):
    import yagmail
    import configparser

    logger.error('', exc_info=(exc_type, exc_value, exc_traceback))

    conf = configparser.ConfigParser()
    conf.read('~/CodeLib/keyring.ini')
    address = conf['mail']['mail']
    key = conf['mail']['key']

    yag = yagmail.SMTP(address, key,host='smtp.qq.com')
    title = 'OA Login Failed'
    # content = (exc_type, exc_value, exc_traceback)
    trace= traceback.format_exception(exc_type, exc_value, exc_traceback)
    content="\n".join(trace)
    yag.send(subject=title, contents=content)

    drv.quit()



# overwrite exception hook
sys.excepthook = callback_func

# =========logging config=============
# init root logger by setting basicConfig
# consoleHandler = logging.StreamHandler(sys.stdout)
# consoleHandler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    # handlers=[fileHandler, consoleHandler],
    # handlers=[consoleHandler],
    encoding='utf8'
)

# Global logger for this module
logger: logging.Logger = logging.getLogger(__name__)

# =========base config=============
now=datetime.datetime.strftime(datetime.datetime.now(),'%Y/%m/%d %H:%M:%S')
logger.info(f'init@ {now}')

url = 'https://iam.cscec8b.com.cn:48101/authn/index.html?service=https%3A%2F%2Fiam.cscec8b.com.cn%3A48101%2Fcas%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3Did230859%26redirect_uri%3Dhttps%253A%252F%252Fapp.cscec8b.com.cn%252Fwelcome-reset-cookie.html%26response_type%3Dcode%26client_name%3DCasOAuthClient'
# new_driver_path = 'path to driver'
# firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

logger.debug(f'goto {url}')
# =========init driver=============
option = FirefoxOptions()
option.set_preference('permissions.default.image', 2)
option.set_preference('permissions.default.stylesheet', 2)
# option.set_preference('javascript.enabled', False)
option.add_argument('--headless')
# option.add_argument('--safe-mode')

drv = Firefox(options=option)
logger.info('drv init')
drv.implicitly_wait(30)
drv.get(url)
logger.info(f'got {drv.title}')

# ========= login =============
logger.info(f'wait for login page...')
# time.sleep(3)
newForm= Wait(drv, 20).until(
    EC.visibility_of_element_located(
        (By.ID,'defaultway_staticpwd')
        )
    )
logger.debug(f'login @{drv.current_url}...')
# drv.find_element(by=By.XPATH, value='//button[@class="more-defaultway ie8borderraidus"]').click()

# drv.switch_to.frame("moreLoginBox")
# newForm = drv.find_element(by=By.XPATH, value='//form[@id="otherway_staticpwd"]')
# newForm = drv.find_element(by=By.ID, value='otherway_staticpwd')

# newForm = drv.find_element(by=By.ID, value='defaultway_staticpwd')
# logger.info(newForm.find_element(by=By.NAME, value="username").get_attribute('placeholder'))
# drv.execute_script('arguments[0].scrollIntoView(true);', newForm)
# drv.switch_to.active_element.send_keys(Keys.TAB)
# logger.info(newForm.find_element(by=By.NAME, value="username").is_displayed())
# logger.info(drv.switch_to.active_element.text)
# exit()
newForm.find_element(by=By.NAME, value="username").send_keys('501A4765')
newForm.find_element(by=By.NAME, value='authcode').send_keys('4765@Cceed')

newForm.find_element(by=By.TAG_NAME, value='button').click()

logger.info(f'wait for login result...')
# time.sleep(10)

# logger.debug(drv.page_source)
# with open('con.html','w') as f:
#     f.write(drv.page_source)
logger.debug(f'now @ {drv.title}: {drv.current_url=}')
Wait(drv, 15).until(
        EC.title_contains('中建八局门户'))
logger.debug(f'now @ {drv.title}: {drv.current_url=}')
# assert drv.title=='中建八局门户'
logger.info(f'logged in')

# ========= view news =============
logger.info('view news')
logger.debug(f'now @ {drv.title}')
logger.debug(f'{drv.current_url=}')

home=drv.current_window_handle
logger.debug(f'{home=}')

logger.info(f'wait for home page loading...')

newsRegion = Wait(drv, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH,f'//div[@id="app"]//div[@class="page-right"]//div[@class="cells_col"][{randint(1,2)}]')
            )
        )
                                         # [randint(0,1)]
# newsRegion = drv.find_elements(by=By.XPATH, value='//div[@id="app"]//div[@class="page-right"]//div[@class="cells_col"]')[randint(0,1)]
newsCell= newsRegion.find_elements(by=By.CLASS_NAME, value='card-cell')[randint(0,3)]
# print(len(newsCell))
logger.info(f"{newsCell.text=}")
newsCell.click()

logger.info(f'wait for news...')
time.sleep(5)
wnds=drv.window_handles
logger.debug(f'{wnds=}')
drv.switch_to.window(wnds[-1])

logger.info(f'reading news...')
time.sleep(3)

logger.info(f'now @ {drv.title}')
logger.debug(f'{drv.current_url=}')
logger.debug(f'{drv.current_window_handle=}')

# ========= log out =============
# drv.close()
# ActionChains(drv).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
logger.info('logout')
drv.switch_to.window(home)
logger.debug(f'{drv.current_window_handle=}')
logger.debug(f'now @ {drv.title}')

drv.find_element(by=By.XPATH,
                 value='//div[@class="page-header-right"]//div[@class="avatar-cell" and position()=5]//div[@class="cell"]'
                 ).click()

drv.find_element(by=By.XPATH, value='//button[@class="ant-btn ant-btn-primary"]').click()
logger.info('finish')
drv.quit()
