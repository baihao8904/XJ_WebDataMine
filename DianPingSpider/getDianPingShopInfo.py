import os
from webDataMine import resource
import random
import requests
import time
from bs4 import BeautifulSoup
import re
import multiprocessing

#需人工登陆大众点评网页验证
def getDianPingShopInfo(line):
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    if not os.path.exists("./ShopInfo"):
        os.mkdir("./ShopInfo")
    time.sleep(3)
    shopName = line.split("\t")[0]
    print('处理' + shopName)
    shopUrl = line.split("\t")[1].strip()
    CommentUrl = shopUrl+"/review_more?pageno="
    print(shopUrl)
    try:
    # proxies = {
    #     'http':random.choice(resource.PROXIES)
    # }
        proxiedDict = {
            "http": 'http://' + random.choice(resource.PROXIES)
        }
        web_data = requests.get(shopUrl, headers=headers, proxies=proxiedDict)
        Soup = BeautifulSoup(web_data.text,'lxml')
        try:
            shopRank = Soup.select("div.comment-rst > span")[0].get('title')
        except:
            shopRank = '系统未对该店做出评级'
        try:
            shopAddress = Soup.select("div.shop-addr > span")[0].get("title")
        except:
            shopAddress='未提供地址'
        try:
            shoptele = Soup.select("div.shopinfor > p > span:nth-of-type(1)")[0].text
            shoptele = re.sub(" ", ' ', shoptele)
        except:
            shoptele = '未提供电话'
        theUrl = CommentUrl+str(1)
        commentData = requests.get(theUrl, headers=headers, proxies=proxiedDict)
        commentSoup = BeautifulSoup(commentData.text,'lxml')
        with open("./ShopInfo/"+shopName+'.txt','a') as _f:
            _f.write(shopName+'\t'+shopRank+'\t'+shopAddress+"\t"+shoptele)
            _f.write("\n")
        totalRank = []
        for item in  commentSoup.select("div.comment-summary.Fix > ul > li"):
            commentrank = item.select("span:nth-of-type(1)")[0].text
            commentPercentage = item.select("span.progress-bar span.bar")[0].text
            commentNums = item.select('a')[0].text
            totalRank.append(commentrank+"\t"+'占比:'+commentPercentage+"\t"+'数量:'+commentNums)
        with open("./ShopInfo/"+shopName+'.txt','a') as _f:
            _f.write("\t".join(totalRank))
            _f.write("\n")
        try:
            pagesOfComment = commentSoup.select("div.Pages > div.Pages > a")[-2].text
        except:
            pagesOfComment = 1
        for i in range(int(pagesOfComment)):
            print('第' + str(i + 1) + '页')
            CommentPageUrl = CommentUrl+str(i+1)
            CommentPageData = requests.get(CommentPageUrl , headers=headers, proxies=proxiedDict)
            CommentPageSoup = BeautifulSoup(CommentPageData.text, 'lxml')
            for item in CommentPageSoup.select('ul > li.comment-list-item'):
                UserName = item.select('div.content > div.user-info > a')[0].text
                UserRank = item.select('div.user-info > span')[0].get('title')
                UserCommentRank = item.select('div.comment-rst > span')[0].get('title')
                UserOthercomment = ''
                try:
                    for rankWay in range(3):
                        theWay = item.select('div.comment-rst > dl > dt:nth-of-type({})'.format(str(rankWay+1)))[0].text
                        UserOthercomment +=theWay
                        theWayRank = item.select('div.comment-rst > dl > dd:nth-of-type({})'.format(str(rankWay+1)))[0].text
                        UserOthercomment+=theWayRank
                except:
                    pass
                CommentContent = item.select("div.comment-entry")[0].text
                    #rat为&nbsp;
                CommentContent = re.sub(" ",' ',CommentContent)
                CommentTime = item.select("div.misc span.time")[0].text
                CommentTime = re.sub(" ",' ',CommentTime)
                try:
                    with open("../ShopInfo/" + shopName + '.txt', 'a') as _f:
                        _f.write('用户名:'+UserName+'\t'+'用户等级:'+UserRank+'\t'+'用户评级:'+UserCommentRank+'\t'+UserOthercomment+'\n')
                        _f.write(CommentContent)
                        _f.write('\n'+'评论时间'+CommentTime)
                        _f.write('\n'+"***************************************************"+'\n')
                except:
                    with open("../ShopInfo/" + shopName + '.txt', 'a') as _f:
                        _f.write('评论有误，请人工查看')
                        _f.write('\n' + "***************************************************" + '\n')
    except:
        print('出错' + shopName)
        thetime = time.strftime('%Y-%m-%d',time.localtime())
        with open('./errorShop'+thetime+'.txt','a+') as fp:
           fp.write(shopName+'\t'+shopUrl+'\n')

def muldeal():
    theFile = '../shopUrl/shopUrl.txt'
    lines = []
    for line in open(theFile).readlines():
        lines.append(line)
    pool = multiprocessing.Pool()
    res = pool.map(getDianPingShopInfo,lines)
    # for item in lines:
    #     getDianPingShopInfo(item)
if __name__ == '__main__':
    muldeal()