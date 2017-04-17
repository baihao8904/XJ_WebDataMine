import os
from webDataMine import resource
import random
import requests
import time
from bs4 import BeautifulSoup
import re
import pymysql


def getDianPingShopInfo(line):
    #数据库connection设置 根据自己情况修改
    #评论数据中有可能会有4位以上字符才能表示的字 所以charset字段需设置为utf8mb4
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='baihao1234',
        db='dianpingdata',
        charset='utf8mb4'
    )

    #设置headers
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    if not os.path.exists("../ShopInfo"):
        os.mkdir("../ShopInfo")
    time.sleep(3)
    #店名
    shopName = line.split("\t")[0]
    print('处理' + shopName)
    shopUrl = line.split("\t")[1].strip()
    #店铺ID 主键
    shopID = int(shopUrl.split('/')[-1])
    CommentUrl = shopUrl+"/review_more?pageno="
    print(shopUrl)
    #设置代理
    proxiedDict={
        "http":'http://180.122.147.23:35650' #+random.choice(resource.PROXIES)
    }
    # try:
    #请求web数据
    web_data = requests.get(shopUrl, headers=headers,proxies=proxiedDict)
    #使用lxml方式进行处理
    Soup = BeautifulSoup(web_data.text,'lxml')
    #商户评级
    try:
        shopRank = Soup.select("div.comment-rst > span")[0].get('title')
    except:
        shopRank = '系统未对该店做出评级'

    #寻找商铺所属地区 商铺所属地区 街道 分类
    try:
        if len(Soup.select('div.breadcrumb b')) > 3:
            shopArea = Soup.select('div.breadcrumb b')[1].select('a span:nth-of-type(1)')[0].text
            shopStreet = Soup.select('div.breadcrumb b')[2].select('a span:nth-of-type(1)')[0].text
            shopClasscify = Soup.select('div.breadcrumb b')[3].select('a span:nth-of-type(1)')[0].text
        elif len(Soup.select('div.breadcrumb b')) == 3:
            shopArea = Soup.select('div.breadcrumb b')[1].select('a span:nth-of-type(1)')[0].text
            shopStreet = '无'
            shopClasscify = Soup.select('div.breadcrumb b')[2].select('a span:nth-of-type(1)')[0].text
        elif len(Soup.select('div.breadcrumb a'))>=3:
            shopArea = Soup.select('div.breadcrumb a')[1].text
            shopStreet = Soup.select('div.breadcrumb a')[1].text
            shopClasscify = Soup.select('div.breadcrumb a')[2].text
    except:
        shopArea = '无'
        shopStreet = '无'
        shopClasscify = '无'
    #商户地址
    try:
        shopAddress = Soup.select("div.shop-addr > span")[0].get("title")
    except:
        try :
            shopAddress=Soup.select('dl.shopDeal-Info-address > dd > span:nth-of-type(1)')[0].text
        except:
            shopAddress = '未提供地址'
    #商户电话
    try:
        shoptele = Soup.select("div.shopinfor > p > span:nth-of-type(1)")[0].text
        shoptele = re.sub(" ", ' ', shoptele)
    except:
        try:
            shoptele = Soup.select("dd.shop-info-content strong")[0].text
            shoptele = re.sub(" ", ' ', shoptele)
        except:
            shoptele = '未提供电话'

    #插入商户基本信息至数据库
        #数据库游标设置
    infocur = connection.cursor()
    theInfoSet = (shopID, shopName,shopRank,shopArea,shopStreet, shopClasscify,shopAddress,shoptele)
    print(theInfoSet)
    insertInfoSql = "INSERT INTO ShopInfo(ShopID,ShopName,ShopRank,ShopArea,ShopStreet,ShopClasscify,ShopAddress,ShopTele) \
                                    values(%s,%s,%s,%s,%s,%s,%s,%s)"
    infocur.execute(insertInfoSql,theInfoSet)
    infocur.close()

    #商户评论分析
    commentData = requests.get(CommentUrl+str(1), headers=headers)
    commentSoup = BeautifulSoup(commentData.text,'lxml')
    totalRank = [shopID,shopName]
    #建立评论星级表单独存储
    for item in  commentSoup.select("div.comment-summary.Fix > ul > li"):
        try:
            #commentrank = item.select("span:nth-of-type(1)")[0].text
            commentPercentage = item.select("span.progress-bar span.bar")[0].text
            commentNums = item.select('a')[0].text
        except:
            #commentrank = '无'
            commentPercentage = '无'
            commentNums = '无'
        #totalRank.append(commentrank)
        totalRank.append(commentPercentage)
        totalRank.append(commentNums)
    #插入评论星级表
    if len(totalRank)>2:
        rankcur = connection.cursor()
        theRankSet = totalRank
        print(theRankSet)
        insertRankSql = "INSERT INTO ShopRankNum(ShopID,ShopName,FiveStarNum,FiveStarPerCentage,FourStarNum,FourStarPerCentage,ThreeStarNum,ThreeStarPerCentage,TwoStarNum,TwoStarPerCentage,OneStarNum,OneStarPerCentage) \
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        rankcur.execute(insertRankSql, theRankSet)
        rankcur.close()
    #获取总评论页数
    try:
        pagesOfComment = commentSoup.select("div.Pages > div.Pages > a")[-2].text
    except:
        pagesOfComment = 1
    for i in range(int(pagesOfComment)):
        print('第' + str(i + 1) + '页')
        CommentPageUrl = CommentUrl+str(i+1)
        #请求评论数据
        CommentPageData = requests.get(CommentPageUrl , headers=headers)
        CommentPageSoup = BeautifulSoup(CommentPageData.text, 'lxml')
        print(CommentPageUrl)
        for item in CommentPageSoup.select('ul > li.comment-list-item'):
            #用户ID
            UserName = item.select('div.content > div.user-info > a')[0].text
            #用户等级
            UserRank = item.select('div.user-info > span')[0].get('title')
            #用户对店铺评级
            try:
                UserCommentRank = item.select('div.comment-rst > span')[0].get('title')
            except:
                UserCommentRank = '用户未给出评价等级'
            #用户对店铺的评分
            UserOthercomment = ''
            try:
                for rankWay in range(3):
                    theWay = item.select('div.comment-rst > dl > dt:nth-of-type({})'.format(str(rankWay+1)))[0].text
                    UserOthercomment +=theWay
                    theWayRank = item.select('div.comment-rst > dl > dd:nth-of-type({})'.format(str(rankWay+1)))[0].text
                    UserOthercomment+=theWayRank
            except:
                pass
            #评论内容
            CommentContent = item.select("div.comment-entry")[0].text
                #rat为&nbsp;
            CommentContent = re.sub(" ",' ',CommentContent)

            #评论时间
            CommentTime = item.select("div.misc span.time")[0].text
            CommentTime = re.sub(" ",' ',CommentTime)
            # try:
            commentcur = connection.cursor()
            theCommentSet = (shopID,shopName,UserName,UserRank,UserCommentRank,UserOthercomment,CommentContent,CommentTime)
            print(UserName,end=' ')
            print('\n')
            insertCommentSql = "INSERT INTO ShopComment(ShopID,ShopName,CommentUser,UserRank,CommentRank,OtherCommentRank,CommentContent,CommentTime) \
                                                                values(%s,%s,%s,%s,%s,%s,%s,%s)"
            commentcur.execute(insertCommentSql, theCommentSet)
            commentcur.close()
        time.sleep(random.randint(1,2) + random.random())
            # except:
    connection.commit()
    connection.close()
    # except:
    #     #出错地址进行保存 下次从本次保存的文件中爬取
    #     print('出错' + shopName)
    #     thetime = time.strftime('%Y-%m-%d',time.localtime())
    #     with open('./errorShop'+thetime+'.txt','a+') as fp:
    #        fp.write(shopName+'\t'+shopUrl+'\n')
    with open("../shopUrl/havedeal.txt", 'a+') as _f:
        _f.write(line)
        _f.write('\n')

def muldeal():
    theFile = '../shopUrl/shopUrl.txt'
    lines = []
    deallines = []
    for line in open(theFile).readlines():
        lines.append(line)
    #保存已经处理过的 完成断点续传功能
    dealFile = '../shopUrl/havedeal.txt'
    for line in open(dealFile).readlines():
        deallines.append(line)
    if len(deallines)>0:
        for item in deallines:
            if item in lines:
                lines.remove(item)
    for item in lines:
        getDianPingShopInfo(item)
        time.sleep(random.randint(1,3)+random.random())

if __name__ == '__main__':
    muldeal()