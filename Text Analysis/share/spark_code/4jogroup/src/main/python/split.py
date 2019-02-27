from konlpy.tag import Mecab

import re
import codecs
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession

#conf=SparkConf.setMaster("local[*]").setAppName("wwow")
sc=SparkContext("local[*]","wwow")    
spark=SparkSession.builder.master("local").appName("good").getOrCreate()
inputPath="hdfs://master:9000/5month/"
df=spark.read.text(inputPath)  
indice=df.rdd.zipWithIndex()
indice_rev=indice.map(lambda x:x.swap)
indice_DS=indice

indice_draft=indice_rev.flatMapValues(lambda x:x.split(" "))
indice_refine=indice_draft.filter(lambda x:x._2.contains("NNP")).filter(lambda x:x._2.length()>1)
indice_DST=indice_refine.toDF()
outputPath="hdfs://master:9000/output10/"
indice_DST.groupBy("_1").pivot("_2").agg(count("_1")).write.format("com.databricks.spark.csv").save(outputPath) 
   

#sqlContext = SQLContext(sc)   
#spark = SparkSession.builder().appName("HDP Test Job").master("yarn").config("spark.hadoop.fs.defaultFS", "hdfs://master:9000").config("spark.yarn.jars", "hdfs://master:9000/spark/jars/*.zip").config("spark.hadoop.yarn.resourcemanager.address", "master:8032").config("spark.hadoop.yarn.application.classpath",        "$HADOOP_CONF_DIR,$HADOOP_COMMON_HOME/*,$HADOOP_COMMON_HOME/lib/*,$HADOOP_HDFS_HOME/*,$HADOOP_HDFS_HOME/lib/*,$HADOOP_MAPRED_HOME/*,$HADOOP_MAPRED_HOME/lib/*,$HADOOP_YARN_HOME/*,$HADOOP_YARN_HOME/lib/*").config("spark.sql.pivotMaxValues",60000)  