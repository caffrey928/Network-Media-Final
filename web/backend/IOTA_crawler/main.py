# selenium 爬 IOTA tangle

from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


# constants
IOTA_TANGLE = "https://explorer.iota.org/mainnet"  # mainnet
ADDR = "iota1qqlvc9x3whxunu9pacm6zq2jv6mp5a8yz26ppljhe0ftjd6v03qdc45jd4m"  # user account address


class IOTA_crawler:
    def __init__(self):
        """
        -----------IOTA crawler------------
        usage:
        crawler = IOTA_crawler()
        result = crawler.get_balance(addr=<your IOTA addr>)
        note:
        result dict: {"status":status->bool,"balance": balance->float}
        """

        self.search_locator = "search--text-input"
        self.balance_locator_nonezero = "/html/body/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/span[1]"
        self.balance_locator_zero = "/html/body/div/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div[2]"
        self.balance_locator_wait = "addr"
        self.table_locator = "transaction--table"
        self.date_locator = "DATE"
        self.amount_locator = "AMOUNT"
        self.id_date = 0
        self.id_amount = 0
        self.addr = ""

        # driver setting
        self.options = Options()
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        self.options.add_argument("--enable-javascript")
        try:
            # open chrome and maximize window
            # self.browser = webdriver.Chrome(
            #     service=Service(ChromeDriverManager().install()), 
            #     options=self.options
            # )
            self.browser = webdriver.Chrome(
                executable_path="./chromedriver.exe",
                options=self.options
            )
            self.browser.maximize_window()

            # open IOTA tangle explorer
            link = IOTA_TANGLE
            print(f"openinging web: {link}")
            self.browser.get(link)
            # rather than sleep, explicit wait might be a better way for crawler, having more custumization options
            # time.sleep(12)
            try:
                WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, self.search_locator)))
                print("Connected to Tangle")
            except:
                print("IOTA_TANGLE: waitfail")
        except:
            pass
    def get_balance(self, addr=ADDR):  # start crawling
        try:
            self.addr = addr
        except:
            self.addr = ADDR
        status = False
        balance = 0
        try:

            ##find searching element and send ADDRESS
            input_ele = self.browser.find_element(By.CLASS_NAME, self.search_locator)
            input_ele.send_keys(ADDR)
            input_ele.send_keys(Keys.ENTER)
            # time.sleep(5)
            try:
                WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, self.balance_locator_wait)))
            except:
                print("BALANCE: waitfail")

            ## find final balance
            try:
                balance_ele = self.browser.find_element(By.XPATH, self.balance_locator_nonezero)
                balance = float(balance_ele.text[:-3])
            except:
                balance_ele = self.browser.find_element(By.XPATH, self.balance_locator_zero)
                balance = 0.0

            ##find transaction table and get closest transaction time and money
            ##某位成員認為是他的心血，強烈要求不能刪掉:)
            # table = self.browser.find_element(By.CLASS_NAME, self.table_locator)
            # tr_head = table.find_element(By.XPATH, ".//thead/tr")  # tr in thead
            # ths_head = tr_head.find_elements(By.XPATH, ".//th")
            # for index, th_head in enumerate(ths_head):
            #     if th_head.text == self.date_locator:
            #         id_date = index
            #     if th_head.text == self.amount_locator:
            #         id_amount = index
            # tr_body = table.find_element(By.XPATH, ".//tbody/tr")  # tr in thead
            # tds_body = tr_body.find_elements(By.XPATH, ".//td")
            # for index, td_body in enumerate(tds_body):
            #     if index == id_date:
            #         date = td_body.text
            #         # print("DATE: ",end="")
            #         # print(date)
            #     if index == id_amount:
            #         amount = td_body.text
            #         # print("AMOUNT: ",end="")
            #         # print(amount)

            ##use beautiful soup to see full crawling result
            # soup = BeautifulSoup(self.browser.page_source, "html.parser")
            # with open("output.html","w",encoding='utf-8') as f:
            #   f.write(str(soup.prettify()))

            ## after grabbing all resoure by selenium,close browser
            status = True
            print("close browser...")
            # self.browser.close()
            #self.browser.quit()
        except Exception as error:
            print("crawling error: ")
            print(error)
            status = False
            balance = 0
        print(f"status: {status}")
        print(f"balance: {balance}")
        return {"status":status,"balance": balance}


if __name__ == "__main__":
    
    crawler = IOTA_crawler()
    result = crawler.get_balance(addr=ADDR)

    time.sleep(5)

    print("crawl 2")
    ADDR = "iota1qqc9mzff65d8d44y7gp0s4jrt7rdygua2kqmh242apcwhdcw0236sxh6esw"
    result = crawler.get_balance(addr=ADDR)
    crawler.browser.quit()