# -*- coding:utf-8 -*-
    
def gettheWord():    
    dictwords = []
    with open('./worddict.txt','r',encoding='utf-8') as fp:
        for item in fp.readlines():
            dictwords.append(item.strip())
    return dictwords
    
if __name__ == '__main__':
    print(gettheWord())