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


#constants
IOTA_TANGLE = "https://explorer.iota.org/mainnet"  # mainnet
ADDR = "iota1qqlvc9x3whxunu9pacm6zq2jv6mp5a8yz26ppljhe0ftjd6v03qdc45jd4m"  # user account address
class IOTA_crawler():
    def __init__(self, addr=ADDR):
        """
        -----------IOTA crawler------------
        usage:
        crawler = IOTA_crawler(addr=<your IOTA addr>)
        result = crawler.start()
        note:
        result dict: {"balance":balance,"date":date,"amount":amount}
        """
        try:
            self.addr = addr
        except:
            self.addr = ADDR
        self.locator = "search--text-input"
        self.balance_locator = "/html/body/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/span[1]"
        self.table_locator = "transaction--table"
        self.date_locator = "DATE"
        self.amount_locator = "AMOUNT"
        self.id_date = 0
        self.id_amount = 0

        #driver setting
        self.options = Options()
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        self.options.add_argument("--enable-javascript")
    def start(self): #start crawling
        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )
        self.browser.maximize_window()
        #open IOTA tangle explorer
        link = IOTA_TANGLE
        print(f"openinging web: {link}")
        self.browser.get(link)
        time.sleep(12)

        ##find element and send ADDRESS
        input_ele = self.browser.find_element(By.CLASS_NAME,self.locator)
        input_ele.send_keys(ADDR)
        input_ele.send_keys(Keys.ENTER)
        
        time.sleep(5)
        ## find final balance
        balance_ele = self.browser.find_element(By.XPATH,self.balance_locator)
        balance = balance_ele.text
        #print(f"Final balance: {balance_ele.text}")
        ##find transaction table and get closest transaction time and money
        # table = self.browser.find_element(By.CLASS_NAME,self.table_locator)
        # tr_head = table.find_element(By.XPATH,'.//thead/tr') #tr in thead
        # ths_head = tr_head.find_elements(By.XPATH,'.//th')
        # for index,th_head in enumerate(ths_head):
        #     if(th_head.text == self.date_locator):
        #         id_date = index
        #     if(th_head.text == self.amount_locator):
        #         id_amount = index
        # tr_body = table.find_element(By.XPATH,'.//tbody/tr') #tr in thead
        # tds_body = tr_body.find_elements(By.XPATH,'.//td')
        # for index,td_body in enumerate(tds_body):
        #     if(index==id_date):
        #         date = td_body.text
        #         #print("DATE: ",end="")
        #         #print(date)
        #     if(index==id_amount):
        #         amount = td_body.text
        #         #print("AMOUNT: ",end="")
        #         #print(amount)

        #soup = BeautifulSoup(self.browser.page_source, "html.parser")

        #with open("output.html","w",encoding='utf-8') as f:
        #   f.write(str(soup.prettify()))
        ## after grabbing all resoure by selenium,close browser
        print("close browser...")
        self.browser.close()
        # return {"balance":balance,"date":date,"amount":amount}
        return {"balance":balance}
    


if __name__ == "__main__":
    crawler = IOTA_crawler(addr=ADDR)
    result = crawler.start()
    print(result["balance"])
    # print(result["date"])
    # print(result["amount"])
