import logging
import os
import requests
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlencode, quote_plus


logger = logging.getLogger("auxmoney")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

opts = Options()
opts.headless = True
logger.info("Starte FireFox")
browser = Firefox(options=opts)

#Setzen der Variablen
picturepath = os.environ.get('PICTUREPATH', '/tmp/home')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
telegrambotkey = os.environ.get('TELEGRAMBOTKEY')
chatid = os.environ.get('CHATID')

logger.info("Öffne Startseite")

# Startseite
browser.get('https://www.auxmoney.com/login')
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/1.png")
except WebDriverException:
    logger.warning("Bild 1 konnte nicht gespeichert werden.")

#Cookie
browser.find_element_by_xpath('//*[@id="c-right"]/a').click()
time.sleep(10)
browser.find_element_by_id('login_loginUsername').send_keys(username)
browser.find_element_by_id('login_loginPassword').send_keys(password)

# Seite nach Login
browser.find_element_by_id('loginSubmit').submit()
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/2.png")
except WebDriverException:
    logger.warning("Bild 2 konnte nicht gespeichert werden.")

renditeindex = browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[1]/div[1]/div[2]/a/p[2]').text
logger.info("Rendite Index: " + renditeindex)

browser.get('https://www.auxmoney.com/anlegercockpit/returns')
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/3.png")
except WebDriverException:
    logger.warning("Bild 3 konnte nicht gespeichert werden.")

monat = browser.find_element_by_xpath('/html/body/div[1]/main/div/article/div/section[2]/table/tbody/tr[1]/td[1]/strong').text
rueckfluss = browser.find_element_by_xpath('/html/body/div[1]/main/div/article/div/section[2]/table/tbody/tr[1]/td[5]/strong').text
logger.info("Aktueller Rückfluss im " + monat + ": " + rueckfluss)

browser.get('https://www.auxmoney.com/anlegercockpit/investaccount')
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/4.png")
except WebDriverException:
    logger.warning("Bild 4 konnte nicht gespeichert werden.")

kontostand = browser.find_element_by_xpath('/html/body/div[1]/main/div/article/div/table/tbody/tr[3]/td[2]/strong').text
logger.info("Kontostand: " + kontostand)

# Logout
browser.get('https://www.auxmoney.com/logout')
time.sleep(20)
try:
    browser.get_screenshot_as_file(picturepath + "/5.png")
except WebDriverException:
    logger.warning("Bild 5 konnte nicht gespeichert werden.")

browser.quit()

text = "Auxmoney: Rückfluss im " + monat + " sind " + rueckfluss + \
        ". Die Rendite beträgt " + renditeindex + ". " \
        "Kontostand beträgt " + kontostand
payload = {'chat_id': chatid, 'text': text}
result = urlencode(payload, quote_via=quote_plus)
r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
logger.info(r.json())

exit(0)