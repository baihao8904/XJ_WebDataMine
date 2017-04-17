# -*- coding:utf-8 -*-
import numpy
import pandas
import os
from PIL import Image
import wordcloud
import jieba.analyse
import pymysql
import matplotlib.pyplot as plt

def toCloud(shopname,theText,mask_path=None):
    #不先分词 作出的词云就全是句子
    newtext = jieba.cut(theText,cut_all=False)
    strtext = ' '.join(newtext)
    if mask_path != None:
        themask = numpy.array(Image.open(mask_path))
    else:
        themask = None
    CommentwordCloud = wordcloud.WordCloud(font_path='../字体/楷体_GB2312.ttf',mask= themask,max_words=500,max_font_size=40,\
                   background_color='white',stopwords=wordcloud.STOPWORDS.add("said"))
    if not os.path.exists('./wordcloud'):
        os.mkdir('./wordcloud')
    CommentwordCloud.generate(strtext)
    CommentwordCloud.to_file(os.path.join('./wordcloud',shopname+'.jpg'))
    return CommentwordCloud


def findKeyWord(theText):
    newtext = jieba.analyse.extract_tags(theText,topK=15)
    keywordStr = ';'.join(newtext)
    return keywordStr

#笔记本数据库叫datamine 实验室的叫dianpingdata
    
def searchShopAllContent(shopname):
    connection = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'baihao1234',
            db = 'dianpingdata',
            charset = 'utf8mb4'
        )
    cur = connection.cursor()
    sql = "SELECT `CommentContent` FROM `shopcomment` WHERE `ShopName` = '"+shopname+"'"
    cur.execute(sql)
    if cur.fetchone()==None:
        return "请检查输入的店名！"
    totalCommentContent = ''
    for item in cur.fetchall():
        totalCommentContent += item[0].strip()
    return totalCommentContent

def searchShopWorstComment(shopname):
    connection = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'baihao1234',
            db = 'dianpingdata',
            charset = 'utf8mb4'
        )
    cur = connection.cursor()
    sql = "SELECT `CommentContent` FROM `shopcomment` WHERE `Shopname`='"+shopname+"' and `CommentRank` LIKE '%差%'"
    cur.execute(sql)
    if cur.fetchone()==None:
        return "请检查输入的店名！"
    totalworstCommentContent = ''
    for item in cur.fetchall():
        totalworstCommentContent += item[0].strip()
    worsttext = jieba.cut(totalworstCommentContent,cut_all=False)
    strtext = ' '.join(worsttext)
    return strtext



if __name__ == '__main__':
    text = searchShopAllContent('纽约国际儿童俱乐部(高新尚中心)')
    print(findKeyWord(text))
    toCloud('纽约国际儿童俱乐部(高新尚中心)',text,mask_path='./mask.jpg')
    print(searchShopWorstComment('纽约国际儿童'))
    