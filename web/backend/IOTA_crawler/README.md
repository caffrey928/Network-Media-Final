# IOTA web crawler

## Installation

1. environment

```
pip install -r requirement.txt
```

2. Webdriver

- install webdriver 💁 [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
- select right version of your chrome: 💁 more ▶️ help ▶️ more about chrome

4. usage

- Test
- 1. modify your desired address in

```
if __name__ == "__main__":
    #ADDR = your desired address
    crawler = IOTA_crawler()
    result = crawler.get_balance(addr=ADDR)
```

- Import as module
- 1. import module

```
import IOTA_crawler
```

- 2. use it as the way in [Test](#test)
- 3. The `result` has the form:

```
{"status":status->bool,"balance": balance->float}
```
