# coding=utf-8
import time

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
import sys


def callback_func(exc_type, exc_value, exc_traceback):
    import yagmail
    import configparser

    conf = configparser.ConfigParser()
    conf.read('keyring.ini')
    address = conf['mail']['mail']
    key = conf['mail']['key']

    yag = yagmail.SMTP(address, key)
    title = 'OA Login Failed'
    content = (exc_type, exc_value, exc_traceback)
    yag.send(subject=title, contents=content)


# overwrite exception hook
sys.excepthook = callback_func

# =========base config=============
url = 'http://app.cscec8b.com.cn'

# new_driver_path = 'path to driver'
# firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

# =========init driver=============
option = FirefoxOptions()
option.set_preference('permissions.default.image', 2)
option.set_preference('permissions.default.stylesheet', 2)
# option.set_preference('javascript.enabled', False)
# option.add_argument('--headless')

drv = Firefox(options=option)

drv.implicitly_wait(30)
drv.get(url)

# ========= login =============
time.sleep(3)
drv.find_element(by=By.XPATH, value='//button[@class="more-defaultway ie8borderraidus"]').click()

drv.switch_to.frame("moreLoginBox")
# newForm = drv.find_element(by=By.XPATH, value='//form[@id="otherway_staticpwd"]')
newForm = drv.find_element(by=By.ID, value='otherway_staticpwd')
newForm.find_element(by=By.NAME, value="username").send_keys('501A4765')
newForm.find_element(by=By.NAME, value='authcode').send_keys('4765@Cceed')
newForm.find_element(by=By.TAG_NAME, value='button').click()

# ========= view news =============
home = drv.current_window_handle
print(f'{home=}')
print(drv.title)
newsRegion = drv.find_element(by=By.XPATH, value='//div[@id="app"]//div[@class="page-right"]//div[@class="cells_col"]')
newsRegion.find_element(by=By.CLASS_NAME, value='card-cell').click()
time.sleep(10)
# ========= log out =============
# drv.close()
# ActionChains(drv).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
drv.switch_to.window(home)
print(drv.current_window_handle)
print(drv.title)
drv.find_element(by=By.XPATH,
                 value='//div[@class="page-header-right"]//div[@class="avatar-cell" and position()=5]//div[@class="cell"]'
                 ).click()

drv.find_element(by=By.XPATH, value='//button[@class="ant-btn ant-btn-primary"]').click()
drv.quit()
