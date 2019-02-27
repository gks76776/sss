package com.pnu.spark.jogroup


import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.Dataset
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import scala.collection.immutable.Map
object pratice {
   def run(inputPath: String, outputPath: String){
 
   }
   
  def main(args: Array[String]): Unit = {
  val conf=new SparkConf()
    .setMaster("local[3]")
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
     .config("spark.sql.pivotMaxValues",100000)  
/*     .config("spark.driver.memory","5g")
     .config("spark.executor.memory", "4g")
    .enableHiveSupport()*/
.getOrCreate()
     
println("씹지 마라고!!!")

 val inputPath="hdfs://master:9000/sample/"
 val outputPath="hdfs://master:9000/sample_output/"
 val df=spark.read.text(inputPath)
 //print("첫번째주자",df.show(10))
 val indice=df.as(Encoders.STRING).rdd.zipWithIndex()
// print("indice",indice.toDF().show(10))
 val indice_rev=indice.map(_.swap)
 //print("indice_rev",indice_rev.toDF().show(10))
 val indice_DS=indice.toDS()

 val indice_draft=indice_rev.flatMapValues(_.split(" ")) 
 //print("indice_draft",indice_draft.toDF().show(10))
val indice_refine=indice_draft.filter(_._2.contains("NNP")).filter(_._2.length()>1)

val indice_DST=indice_refine.toDS()
print("indice_DST",indice_DST.show(10))
//  println(indice_DST.groupBy($"_1").pivot("_2").agg(count("_1")).na.fill(0).show(10))
 //println(indice_DST.groupBy("_1").pivot("_2").agg(count("_1")).show(10))
//println(indice_rev.toDS().groupBy("_1").pivot("_2").agg(count("_1")).show(5))

 // println("na",indice_DS.na)
    
 // indice_DST.groupBy("_1").pivot("_2").agg(count("_1")).write.format("com.databricks.spark.csv").option("header",true).save(outputPath) 
     }
}