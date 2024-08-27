# coding=utf-8

import sys
import traceback
import time
import logging

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


fileHandler = logging.FileHandler('OaLogin.log', encoding='utf8')
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

# Global logger for this module
logger: logging.Logger = logging.getLogger(__name__)



def callback_func(exc_type, exc_value, exc_traceback):
    import yagmail
    import configparser

    logger.error('', exc_info=(exc_type, exc_value, exc_traceback))

    conf = configparser.ConfigParser()
    conf.read('keyring.ini')
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

# =========base config=============
logger.info('init')
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
logger.debug('drv init')
drv.implicitly_wait(30)
drv.get(url)
logger.debug(f'got {drv.title}')

# ========= login =============
for i in range(3):
    logger.info(f'wait for login page {3-i}...')
    time.sleep(1)
# print()
logger.debug(f'login @{drv.current_url}...')
# drv.find_element(by=By.XPATH, value='//button[@class="more-defaultway ie8borderraidus"]').click()

# drv.switch_to.frame("moreLoginBox")
# newForm = drv.find_element(by=By.XPATH, value='//form[@id="otherway_staticpwd"]')
# newForm = drv.find_element(by=By.ID, value='otherway_staticpwd')

newForm = drv.find_element(by=By.ID, value='defaultway_staticpwd')
# print(newForm.find_element(by=By.NAME, value="username").get_attribute('placeholder'))
# drv.execute_script('arguments[0].scrollIntoView(true);', newForm)
# drv.switch_to.active_element.send_keys(Keys.TAB)
# print(newForm.find_element(by=By.NAME, value="username").is_displayed())
# print(drv.switch_to.active_element.text)
# exit()
newForm.find_element(by=By.NAME, value="username").send_keys('501A4765')
newForm.find_element(by=By.NAME, value='authcode').send_keys('4765@Cceed')

newForm.find_element(by=By.TAG_NAME, value='button').click()

for i in range(10):
    logger.debug(f'wait for login result {10-i}...')
    time.sleep(1)
# print()

logger.debug(f'logged in to {drv.title}')
logger.debug(f'{drv.current_url=}')
# with open('con.html','w') as f:
#     f.write(drv.page_source)
# assert drv.title=='中建八局门户'

# ========= view news =============
logger.info(f'now @ {drv.title}')
logger.debug(f'{drv.current_url=}')

home=drv.current_window_handle
logger.debug(f'{home=}')

logger.info('open news')
newsRegion = drv.find_element(by=By.XPATH, value='//div[@id="app"]//div[@class="page-right"]//div[@class="cells_col"]')
newsCell=newsRegion.find_element(by=By.CLASS_NAME, value='card-cell')
logger.info(f"{newsCell.text=}")
newsCell.click()


for i in range(10):
    logger.debug(f'wait for news {10-i}...')
    time.sleep(1)
# print()

wnds=drv.window_handles
logger.debug(f'{wnds=}')
drv.switch_to.window(wnds[-1])
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
