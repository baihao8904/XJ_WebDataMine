# GaoDeSpider
高德地图的数据爬取

1,getXDaili
  调用讯代理API生成代理。调用频率需低于15秒一次
  
2,DownLoadGaoDeJson
  输入参数：（1）关键词 构成查询url 在get请求时，调用quote方法转化成url编码
            （2）关键词拼音 生成存储路径
  功能：将相应关键词对应的json文件存储到本地。
  
3，getGaoDeGetShopId
   输入参数：json文件的存储路径
   功能：处理json数据，获取商铺的名称和ID，方便构造商铺url
   
4，getGaoDeShopInfo
   输入参数：存储ID的txt的路径
   功能：根据商铺URL，获取商铺信息和评论信息。每十家商铺自动生成新代理。
           获取的信息存储在mysql中。
