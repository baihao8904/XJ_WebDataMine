import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import GaoDeSpider.getXDaili
from urllib.parse import quote

def getJson(QueryName,QueryPinyin):
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    page = 1
    thepath = './GaoDeFile/jsonfile/'+QueryPinyin
    if not os.path.exists(thepath):
        os.mkdir(thepath)
    proxiedDict = GaoDeSpider.getXDaili.getDaili()
    proxy = urllib.request.ProxyHandler(proxiedDict)
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    while True:
        url = 'http://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum={}' \
              '&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000' \
              '&addr_poi_merge=true&is_classify=true&zoom=12&city=610100' \
              '&geoobj=108.755763%7C34.165071%7C109.250148%7C34.366805&keywords={}'.format(str(page),quote(QueryName))
        web_Data = requests.get(url,headers=headers,proxies = proxiedDict)
        Soup = BeautifulSoup(web_Data.text,'lxml')
        theStr = str(Soup)
        pattern = '"change_query_tip":"(.*?)"'
        result = re.compile(pattern).findall(theStr)
        if len(result[0])>0:
            break
        print('存储第'+str(page)+'页')
        local = os.path.join(thepath,QueryName+str(page)+'.json')
        urllib.request.urlretrieve(url,local)
        page+=1
        
def showJson():
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    page = 1
    url = 'http://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum={}' \
              '&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=610100&geoobj=108.755763%7C34.165071%7C109.250148%7C34.366805&keywords=%E6%97%A9%E6%95%99'.format(str(page))
    web_Data = requests.get(url,headers=headers)
    Soup = BeautifulSoup(web_Data.text,'lxml')
    print(Soup)
    
if __name__ =="__main__":
    getJson('幼儿教育','YouErJiaoYu')