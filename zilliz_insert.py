import json
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# 连接集群
connections.connect(
  alias='default', 
  #  从控制台获取的集群公网地址
  uri='https://in01-94079557b590a23.ali-cn-hangzhou.vectordb.zilliz.com.cn:19530',
  secure=True,
  token='db_admin:Gao6584802@', # 创建集群时指定的用户名和密码
        # 也可以使用旧连接方式 `user` 和 `password` 来替代 `token`：
        # user='',
        # password='' 
)

fields = [
	FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="animaltype", dtype=DataType.VARCHAR,  max_length=30, is_primary=False),
    FieldSchema(name="quest", dtype=DataType.VARCHAR, max_length=512, is_primary=False),  
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=512, is_primary=False), 
    FieldSchema(name="quest_vector", dtype=DataType.FLOAT_VECTOR, dim=2)    
]


# 3. 创建 Schema
schema = CollectionSchema(
    fields,
    description="Schema of pet question_answers",
    enable_dynamic_field=False
)

# 4. 创建 Collection
collection = Collection(
    name="pet_question", 
    description="pet question",
    schema=schema
)

# 5. 创建索引

index_params = {
    "index_type": "AUTOINDEX",
    "metric_type": "L2",
    "params": {}
}


# 创建特定名称的索引：
collection.create_index(
  field_name="quest_vector", 
  index_params=index_params,
  index_name='quest_vector_index'
)


# 6. 加载 Collection
collection.load()


# 查看加载进程
progress = utility.loading_progress("pet_question")

print(f"Collection loaded successfully: {progress}")

collection.release()

# with open('/path/to/downloaded/medium_articles_2020_dpr.json') as f:
#         data = json.load(f)
#         rows = data['rows'][0:200]

# print(rows[:2])


# import pandas as pd
# #1.读取前n行所有数据
# df1=pd.read_excel('data.xlsx')#读取xlsx中的第一个sheet
# # data1=df1.head(10)#读取前10行所有数据
# data2=df1.values#list【】  相当于一个矩阵，以行为单位


# jsdata ={}
# rows = []

# for row in data2:
#     # quest_dict = {"id": row[0],"animaltype": row[1],"quest":row[2],"answer":row[3],"quest_vector":[0.04347792807504089,0.04631808562900841]}
#     quest_dict = {"id": row[0],"animaltype": row[1],"quest":row[2],"answer":row[3]}
#     rows.append(quest_dict)
# jsdata ={"rows":rows }
# # print(jsdata)

# results = collection.insert(jsdata)
# collection.flush()
# print(f"Data inserted successfully! Inserted rows: {results.insert_count}")