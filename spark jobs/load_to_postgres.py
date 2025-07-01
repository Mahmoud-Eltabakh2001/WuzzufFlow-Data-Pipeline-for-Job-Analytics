from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Load HDFS to Postgres") \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.7.7.jar") \
    .getOrCreate()


#read data 
df_jobs = spark.read.option("header", True).option("inferSchema", True).csv("hdfs://namenode:8020/wuzzuf_output/Wuzzuf_data_transformed/*.csv")
df_skills = spark.read.option("header", True).option("inferSchema", True).csv("hdfs://namenode:8020/wuzzuf_output/skills/*.csv")

#load data
df_jobs.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/job_data") \
        .option("dbtable", "jobs") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

df_skills.write \
         .format("jdbc") \
         .option("url", "jdbc:postgresql://postgres:5432/job_data") \
         .option("dbtable", "skills") \
         .option("user", "airflow") \
         .option("password", "airflow") \
         .option("driver", "org.postgresql.Driver") \
         .mode("append") \
         .save()