import requests
from bs4 import BeautifulSoup
import time
import pymysql
import json
import numpy
import os
import traceback
import GaoDeSpider.getXDaili



def getIDList(path):
    ShopIDList = []
    with open(path,'r',encoding="utf-8") as _f:
        for line in _f.readlines():
            shopID = line.split('\t')[1].strip()
            ShopIDList.append(shopID)
    return ShopIDList

def getShopInfo(path):
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='baihao1234',
        db='gaodedata',
        charset='utf8mb4'
    )
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

    if not os.path.exists('./GaoDeFile/dealShop.txt'):
        deallist = []
    else:
        deallist = []
        with open('./GaoDeFile/dealShop.txt','r',encoding='utf-8') as _f:
            for line in _f.readlines():
                deallist.append(line.strip())
    ShopList = getIDList(path)
    restShop = list(set(ShopList)-set(deallist))
    count =0
    proxiedDict = GaoDeSpider.getXDaili.getDaili()
    print('自动生成代理', proxiedDict)
    for theid in ShopList:
        print()
        count+=1
        time.sleep(numpy.random.random_integers(1,4))
        if count % 10==0:
            proxiedDict = GaoDeSpider.getXDaili.getDaili()
            print('自动生成新代理',proxiedDict)
        theURL = "http://ditu.amap.com/detail/{}?citycode=610100".format(theid)
        # theURL = "http://ditu.amap.com/detail/B0FFGA2FRE?citycode=610100"
        try:
            #,proxies=proxiedDict
            web_data = requests.get(theURL,headers=headers,proxies=proxiedDict)
            Soup = BeautifulSoup(web_data.text,'lxml')
            print(theURL)
            ShopName = Soup.select('div.detail_info h4.detail_title')[0].text
            print('正在处理'+ShopName)
            ShopStar = Soup.select("div.detail_description p span.score")
            if len(ShopStar)>0:
                ShopStar = ShopStar[0].text
            else:
                ShopStar = 'Unknown'
            ShoptargetList = Soup.select("div.detail_description p span.tag_2")
            if len(ShoptargetList)>0:
                Shoptarget = ShoptargetList[0].text
            else:
                Shoptarget = 'Unknown'
            ShopteleList = Soup.select("div.detail_description p span.telephone_2")
            if len(ShopteleList)>0:
                Shoptele = ShopteleList[0].text
            else:
                Shoptele = 'Unknown'
            ShopaddList = Soup.select("div.detail_description p span.address_2")
            if len(ShopaddList)>0:
                Shopadd = ShopaddList[0].text
            else:
                Shopadd = 'Unknown'

            infocur = connection.cursor()
            theInfoSet = (theid, ShopName, ShopStar, Shoptarget,Shopadd,Shoptele)
            insertInfoSql = "INSERT INTO shopinfo(ShopGaoDeID,ShopName,ShopRank,ShopTag,ShopAdd,ShopTele) \
                                                values(%s,%s,%s,%s,%s,%s)"
            infocur.execute(insertInfoSql, theInfoSet)
            infocur.close()

            commentNumUrl = 'http://ditu.amap.com/detail/get/reviewList?poiid={}'.format(theid)
            # commentNumUrl = 'http://ditu.amap.com/detail/get/reviewList?poiid=B0FFGA2FRE'
            getJson = requests.get(commentNumUrl)
            Soup = BeautifulSoup(getJson.text,'lxml')
            thejsonstr = Soup.select('p')[0].text
            theJson = json.loads(thejsonstr)
            theCommentNum = theJson['data']['new_count']
            print('该店的评论数量为'+str(theCommentNum))
            if theCommentNum>0:
                theCommentPage = theCommentNum//10+1
                print('正在处理评论')
                for i in range(1,theCommentPage+1):
                    commentUrl = commentNumUrl+"&pagesize=10&pagenum={}&select_mode=4".format(str(i))
                    # commentUrl = 'http://ditu.amap.com/detail/get/reviewList?poiid=B0FFGA2FRE&pagesize=10&pagenum=1&select_mode=4'
                    commentWeb_data = requests.get(commentUrl,headers=headers,proxies=proxiedDict)
                    commentSoup = BeautifulSoup(commentWeb_data.text,'lxml')
                    commentJson = json.loads(commentSoup.select('p')[0].text)
                    commentList = commentJson['data']['review_list']
                    for item in commentList:
                        commentUser = item['author']
                        commentContent = item['review']
                        commentRank = item['score']
                        commentTime = item['time']

                        commentcur = connection.cursor()
                        theCommentSet = (
                        theid, commentUser, commentRank,commentContent, commentTime)
                        insertCommentSql = "INSERT INTO shopcomment(ShopGaoDeID,CommentUser,CommentRank,CommentContent,CommentTime) \
                                                                                        values(%s,%s,%s,%s,%s)"
                        commentcur.execute(insertCommentSql, theCommentSet)
                        commentcur.close()
            deallist.append(theid)
        except:
            print('出错',theid)
            traceback.print_exc()
    connection.commit()
    connection.close()
    with open('./GaoDeFile/dealShop.txt','w') as fp:
        for item in deallist:
            fp.write(item)

if __name__ == '__main__':
    print('./GaoDeFile/ZaoJiao/shopID.txt')
    thepath = input('输入ID文件路径：（上面是例子）')
    getShopInfo(thepath)