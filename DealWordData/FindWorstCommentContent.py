# -*-coding:utf-8 -*-
__author__ = 'lenovo'
import numpy
import pandas
import os
from PIL import Image
import wordcloud
import jieba.analyse
import jieba.posseg
import pymysql

def searchShopWorstComment(shopname):
    connection = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'baihao1234',
            db = 'datamine',
            charset = 'utf8mb4'
        )
    cur = connection.cursor()
    sql = "SELECT `CommentContent` FROM `shopcomment` WHERE `Shopname`='"+shopname+"' and `CommentRank` LIKE '%差%'"
    cur.execute(sql)
    if cur.fetchone()==None:
        return "请检查输入的店名！"
    cur.execute(sql)
    totalworstCommentContent = ''
    for item in cur.fetchall():
        totalworstCommentContent += item[0].strip()
    return totalworstCommentContent

def FindtheWorstCommentContent(aShopTotalWorstComment):
    posgList = []
    wordslist = []
    resultlist = []
    words = jieba.posseg.lcut(aShopTotalWorstComment)
    for word,flag in words:
        wordslist.append(word)
        posgList.append(flag)
    for i in range(len(posgList)):
        if posgList[i] == 'zg':
            if posgList[i+1] == 'n' or posgList[i+1]=='a':
                resultlist.append([i,i+1])
            elif posgList[i+1] == 'v':
                if posgList[i+2]=='a':
                    resultlist.append([i,i+1,i+2])
                else:
                    resultlist.append([i,i+1])
            else:
                continue
        elif posgList[i] == 'l' or posgList[i]=='i':
            if posgList[i+1] == 'v':
                resultlist.append([i,i+1])
            elif posgList[i-1]=='v':
                resultlist.append([i-1,i])
            else:
                resultlist.append([i])
        elif posgList[i] == 'n':
            if posgList[i+1] == 'd':
                if posgList[i+2] == 'a' or posgList[i+2] == 'v':
                    if posgList[i+2]=='v' and posgList[i+3]=='v':
                        resultlist.append([i,i+1,i+2,i+3])
                    else:
                        resultlist.append([i,i+1,i+2])
            elif posgList[i+1] == 'v' and  posgList[i+2] =='n':
                if  posgList[i+3] == 'ul':
                    resultlist.append([i,i+1,i+2,i+3])
                else:
                    resultlist.append([i,i+1,i+2])
            elif posgList[i+1] == 'a' or posgList[i+1] =='v' and posgList[i+2]=='x' and posgList[i-1]!='v':
                resultlist.append([i,i+1])
            elif posgList[i+1]=='nr':
                resultlist.append([i,i+1])
        elif posgList[i] =='b':
            if posgList[i+1] == 'a':
                resultlist.append([i,i+1])
        elif posgList[i] == 'd' and posgList[i-1]!='n':
            if posgList[i+1]=='a' or posgList[i+1] == 'v' and posgList[i+2]!='v':
                if posgList[i+2]=='n' or posgList[i+2]=='ul':
                    resultlist.append([i,i+1,i+2])
                elif posgList[i+2]=='r':
                    if posgList[i+3]!='r':
                        resultlist.append([i,i+1,i+2,i+3])
                    else:
                        pass
                elif posgList[i+2]=='p':
                    resultlist.append([i,i+1,i+2,i+3])
                elif posgList[i+2]!='d':
                    if posgList[i+2] == 't':
                        resultlist.append([i,i+1,i+2])
                    elif posgList[i-1]!='v':
                        resultlist.append([i,i+1])
            if posgList[i+1] == 'n' and posgList[i+2]=='ul':
                resultlist.append([i,i+1,i+2])
            if posgList[i+1] == 'd' and posgList[i+2]=='x':
                resultlist.append([i,i+1])
        elif posgList[i]=='v':
            if posgList[i+1]=='v':
                if posgList[i+2]=='n' or posgList[i+2]=='ul':
                    resultlist.append([i,i+1,i+2])
                elif posgList[i+2]=='x':
                    resultlist.append([i,i+1])
            elif posgList[i+1] == 'n':
                if (posgList[i+2] == 'ul' or posgList[i+2]=='r' or posgList[i+2] =='v') and posgList[i-1]!='n':
                    resultlist.append([i,i+1,i+2])
            elif posgList[i+1] == 'nz':
                resultlist.append([i,i+1])
    strList = []
    for item in resultlist:
        theComment = ''
        for i in range(len(item)):
            theComment += wordslist[item[i]]
        strList.append(theComment)
    thekeywordlist = list(set(strList))
    print(thekeywordlist)
    return thekeywordlist
    
if __name__ == '__main__':
    astr = searchShopWorstComment('澳洲袋鼠国际早教(凯德中心店)')
    FindWorstCommentContent(astr)