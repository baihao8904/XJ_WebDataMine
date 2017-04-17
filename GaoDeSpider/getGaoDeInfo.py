import os
import json

def getInfoFromJson(path):
    dir_list = os.listdir(path)
    num =0
    for item in dir_list:
        filepath = os.path.join(path,item)
        with open(filepath,'r',encoding='utf-8') as _f:
            theJsonfile = json.load(_f)
            for shop in theJsonfile['data']['poi_list']:
                print(shop['id'])
                print(shop['name'])
                num+=1
                with open('./GaoDeFile/shopId.txt','a+') as fp:
                    fp.write(shop['name']+'\t'+shop['id'])
                    fp.write('\n')
    print('共计'+str(num)+'个商家')

if __name__ == '__main__':
    getInfoFromJson('./GaoDeFile/jsonfile/ZaoJiao')