# -*- coding:utf-8 -*-
    
def gettheWord():    
    dictwords = []
    with open('./stoplist.txt','r',encoding='utf-8') as fp:
        for item in fp.readlines():
            dictwords.append(item.strip())
    dictwords.insert(1,'\n')
    dictwords.insert(1,'\xa0')
    dictwords.insert(1,'，')
    return dictwords
    
if __name__ == '__main__':
    print(gettheWord())