import os
from webDataMine import resource
import random
import requests
import time
from bs4 import BeautifulSoup

class getDianPingShopID(object):
    def __init__(self):
        self.hosturl = "http://www.dianping.com/search/category/17/70/g188{}"
        self.shopurl = "http://www.dianping.com"
        self.headers = {
    'Connection':'keep-alive',
    'Content-Type':'text/html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def mkPath(self):
        path = "./shopUrl"
        if not os.path.exists(path):
            os.mkdir(path)

    def Spider(self,page=1):
        self.mkPath()
        for i in range(1,page+1):
            time.sleep(3)
            print('正在处理'+str(i)+'页.')
            hosturl = self.hosturl.format("p"+str(i))
            #proxies=random.choice(resource.PROXIES)
            web_data = requests.get(hosturl,headers = self.headers)
            Soup = BeautifulSoup(web_data.text,'lxml')
            for item in Soup.select('ul.shop-list > li > a'):
                shopName = item.get("alt")
                shopID = item.get("href")
                shopUrl = self.shopurl+shopID
                with open('../shopUrl/shopUrl.txt','a+') as _f:
                    _f.write(shopName+'\t'+shopUrl)
                    _f.write("\n")
        print('处理完毕')

if __name__ == '__main__':
    dianpingspider = getDianPingShopID()
    dianpingspider.Spider(50)