# selenium 爬 IOTA tangle

from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# constans, should in another file, but I am lazy LOL
IOTA_TANGLE = "https://explorer.iota.org/mainnet"  # mainnet
ADDR = "iota1qzn3hw9ptvfxnh9w3adxdkqt0ryrgzcny3eafs0v76ad0hl3v3vrjj9hkc5"  # user account address
locator = "search--text-input"
balance_locator = "/html/body/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/span[1]"
table_locator = "transaction--table"
date_locator = "DATE"
id_date = 0
amount_locator = "AMOUNT"
id_amount = 0

#driver setting
options = Options()
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"]
)
options.add_argument("--enable-javascript")
browser = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
browser.maximize_window()
#open IOTA tangle explorer
link = IOTA_TANGLE
print(f"opening web: {link}")
browser.get(link)
# start crawling
# try:

time.sleep(12)

##find element and send ADDRESS
input_ele = browser.find_element(By.CLASS_NAME,locator)
input_ele.send_keys(ADDR)
input_ele.send_keys(Keys.ENTER)
time.sleep(5)

## find final balance
balance_ele = browser.find_element(By.XPATH,balance_locator)
print(f"Final balance: {balance_ele.text}")
##find transaction table and get closest transaction time and money
table = browser.find_element(By.CLASS_NAME,table_locator)
tr_head = table.find_element(By.XPATH,'.//thead/tr') #tr in thead
ths_head = tr_head.find_elements(By.XPATH,'.//th')
for index,th_head in enumerate(ths_head):
    if(th_head.text == date_locator):
        id_date = index
    if(th_head.text == amount_locator):
        id_amount = index


tr_body = table.find_element(By.XPATH,'.//tbody/tr') #tr in thead
tds_body = tr_body.find_elements(By.XPATH,'.//td')
for index,td_body in enumerate(tds_body):
    if(index==id_date):
        print("DATE: ",end="")
        print(td_body.text)
    if(index==id_amount):
        print("AMOUNT: ",end="")
        print(td_body.text)

#r1 = table.find_element(By.XPATH,'.//tr')
soup = BeautifulSoup(browser.page_source, "html.parser")

with open("output.html","w",encoding='utf-8') as f:
    f.write(str(soup.prettify()))
## after grabbing all resoure by selenium,close browser
print("close browser...")
#browser.close()


# except TimeoutException:
#     print("ERROR")
