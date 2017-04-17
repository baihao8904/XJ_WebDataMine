import requests
from bs4 import BeautifulSoup
import json

def getDaili():
    dailiurl = 'http://www.xdaili.cn/ipagent//privateProxy/getDynamicIP/DD20174171103qUOKsS/5d024dbc0a2c11e7a12d00163e1a31c0?returnType=2'
    webdata = requests.get(dailiurl)
    Soup = BeautifulSoup(webdata.text,'lxml')
    theJson = json.loads(Soup.select('p')[0].text)
    theDaili = 'http://'+theJson['RESULT']['wanIp']+':'+theJson['RESULT']['proxyport']
    proxiedDict = {
            "http": theDaili  # +random.choice(resource.PROXIES)
        }
    return proxiedDict

if __name__ == '__main__':
    print(getDaili())