from webDataMine import resource
import random
import requests
import time
from bs4 import BeautifulSoup


headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
proxiedDict = {
    "http": 'http://60.19.232.203:25628'
}

shopUrl = 'http://www.dianping.com/shop/69939977'
shopID = int(shopUrl.split('/')[-1])
web_data = requests.get(shopUrl, headers=headers, proxies=proxiedDict)
Soup = BeautifulSoup(web_data.text,'lxml')
print(len(Soup.select('div.breadcrumb b')))
try:
    if len(Soup.select('div.breadcrumb b')) > 3:
        shopArea = Soup.select('div.breadcrumb b')[1].select('a span:nth-of-type(1)')[0].text
        shopStreet = Soup.select('div.breadcrumb b')[2].select('a span:nth-of-type(1)')[0].text
        shopClasscify = Soup.select('div.breadcrumb b')[3].select('a span:nth-of-type(1)')[0].text
    elif len(Soup.select('div.breadcrumb b')) == 3:
        shopArea = Soup.select('div.breadcrumb b')[1].select('a span:nth-of-type(1)')[0].text
        shopStreet = ''
        shopClasscify = Soup.select('div.breadcrumb b')[2].select('a span:nth-of-type(1)')[0].text
except:
    shopArea = ''
    shopStreet = ''
    shopClasscify = ''

print(shopArea,shopStreet,shopClasscify,shopID)