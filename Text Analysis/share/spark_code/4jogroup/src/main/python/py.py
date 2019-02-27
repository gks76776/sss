from konlpy.tag import Mecab
from pymongo import MongoClient
import re
import codecs

m = Mecab()
# 이름 있는 DB collection에 대하여 텍스트 파일 출력
#MongoDB 세팅
client = MongoClient()

db = client.news_naver
# 7월 기사에 대하여
coll = db.enter2018_07
conf=SparkConf(master="local[*]",appName="wwow")
sc=SparkContext(conf)    
sqlContext = SQLContext(sc)   
spark = SparkSession.builder().appName("HDP Test Job").master("yarn").config("spark.hadoop.fs.defaultFS", "hdfs://master:9000").config("spark.yarn.jars", "hdfs://master:9000/spark/jars/*.zip").config("spark.hadoop.yarn.resourcemanager.address", "master:8032").config("spark.hadoop.yarn.application.classpath",        "$HADOOP_CONF_DIR,$HADOOP_COMMON_HOME/*,$HADOOP_COMMON_HOME/lib/*,$HADOOP_HDFS_HOME/*,$HADOOP_HDFS_HOME/lib/*,$HADOOP_MAPRED_HOME/*,$HADOOP_MAPRED_HOME/lib/*,$HADOOP_YARN_HOME/*,$HADOOP_YARN_HOME/lib/*").config("spark.sql.pivotMaxValues",60000)  

for doc in coll.find() :
    
    name = str(doc['name'])
    title = doc['title']
    content = doc['content']
    comment = doc['comment']
    
    # 속성에 있는 이름값으로 초기화
    f = codecs.open("article/"+name+".txt", 'w', 'utf-8')

    # 타이틀 형태소
    title = title.replace('\n', '')
    title = title.replace('\t', '')
    title = title.strip()

    for s in m.pos(title):
        if(s[1][0] == 'S'):
            continue
        f.write(s[0]+","+s[1])
        f.write(" ")
    f.write("\n")
    
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.strip()

    # 본문 형태소
    for s in m.pos(content):
        if(s[1][0] == 'S'):
            continue
        f.write(s[0]+","+s[1])
        f.write(" ")
    f.write("\n")

    #comment 형태소
    for c in comment :

        c = c.replace('작성자에 의해 삭제된 댓글입니다.', '')
        c = c.strip()
        if len(c) <= 1:
            continue

        for s in m.pos(c):
            if(s[1][0] == 'S'):
                continue
            f.write(s[0]+","+s[1])
            f.write(" ")
        f.write("\n")


    f.close()
print("텍스트로 변환 완료!")