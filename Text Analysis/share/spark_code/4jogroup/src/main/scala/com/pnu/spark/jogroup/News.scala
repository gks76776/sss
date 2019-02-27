package com.pnu.spark.jogroup

import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf

object News {
  
  //매달 1일 전월의 키워드 분석을 실시한다.
  
  //파이썬 크롤링
  //spark 데이터처리
  //R machine learning
  //웹서버에 전달.(또는 fshell로 cat하면 되지 않을까 싶다.)
  
  def main(args: Array[String]): Unit = {
       val conf=new SparkConf().setMaster("local[*]")
  
   .set("spark.shuffle.service.enabled", "false")

  .set("spark.dynamicAllocation.enabled", "false")

  .set("spark.io.compression.codec", "snappy")

  .set("spark.rdd.compress", "true")
  // .setJars()
   .setAppName("wow")
  val sc=new SparkContext(conf)    
         val sqlContext = new org.apache.spark.sql.SQLContext(sc)
  import sqlContext.implicits._    
     val spark = SparkSession.builder()
    /* .config("spark.driver.memory","5g")
     .config("spark.executor.memory", "4g")*/
     .appName("HDP Test Job")
    .master("yarn")
    .config("spark.hadoop.fs.defaultFS", "hdfs://master:9000")
    .config("spark.yarn.jars", "hdfs://master:9000/spark/jars/*.zip")
    .config("spark.hadoop.yarn.resourcemanager.address", "master:8032")
    .config("spark.hadoop.yarn.application.classpath", 
       "$HADOOP_CONF_DIR,$HADOOP_COMMON_HOME/*,$HADOOP_COMMON_HOME/lib/*,$HADOOP_HDFS_HOME/*,$HADOOP_HDFS_HOME/lib/*,$HADOOP_MAPRED_HOME/*,$HADOOP_MAPRED_HOME/lib/*,$HADOOP_YARN_HOME/*,$HADOOP_YARN_HOME/lib/*")
     .config("spark.sql.pivotMaxValues",60000)  
/*     .config("spark.driver.memory","5g")
     .config("spark.executor.memory", "4g")
    .enableHiveSupport()*/
.getOrCreate()

var inputPath="hdfs://master:9000/5month/"
//val df=spark.read.csv(inputPath)  
val df=spark.read.option("header","true").csv(inputPath)  


df.createOrReplaceGlobalTempView("News")
//println(spark.sql("select 제목 from global_temp.News").show())
println(df.count())
val df_drop=df.select('제목).na.drop()
println(df_drop.show(50))
println(df.count())

//println(df.show())













  }
}