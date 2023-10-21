# 初始化 MilvusClient 实例
# 替换为实际的公网地址和用户名密码
from pymilvus import MilvusClient

client = MilvusClient(
        uri="https://in01-94079557b590a23.ali-cn-hangzhou.vectordb.zilliz.com.cn:19530", # 从控制台获取的集群公网地址
        token="db_admin:Gao6584802#" # 创建集群时指定的用户名和密码
        # 也可以使用旧连接方式 `user` 和 `password` 来替代 `token`：
        # user='',
        # password='' 
)

# 创建 Collection
client.create_collection(
        collection_name="medium_articles",
        dimension=768
)


client.insert(
        collection_name="medium_articles",
        data:{
                "id": 0,
                "title": "The Reported Mortality Rate of Coronavirus Is Not Important",
                "vector": [0.041732933, 0.013779674, ...., -0.013061441],
                "link": "<https://medium.com/swlh/the-reported-mortality-rate-of-coronavirus-is-not-important-369989c8d912>",
                "reading_time": 13,
                "publication": "The Startup",
                "claps": 1100,
                "responses": 18
  			}
)