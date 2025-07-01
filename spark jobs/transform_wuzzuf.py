from pyspark.sql import SparkSession
from pyspark.sql.functions import col,udf,trim,split,size,explode,row_number,regexp_replace,when
from pyspark.sql.window import Window
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,ArrayType
spark=SparkSession.builder.appName("Mahmoud").getOrCreate()


schema= StructType( [StructField("job_title",StringType()),StructField("company_name",StringType()),
                     StructField("company_page",StringType()),StructField("location",StringType()),StructField("job_type",StringType()),
                      StructField("Experience Level",StringType()),StructField("Yrs of Exp",StringType()),StructField("skills",StringType())])
df = spark.read.csv(
    path="hdfs://namenode:8020/wuzzuf/Wuzzuf_data.csv",
    header=True,
    schema=schema
)

window = Window.orderBy("job_title")

df1 = df.withColumn("id", row_number().over(window))

columns=[i for i in df1.columns]
for c in columns:
    if c=="id":
      continue
    else:
      df2=df1.withColumn(c,trim(col(c)))


def company_name(x):
    try:
        return x[:-1].strip()
    except:
        return None


company_name_udf=udf(company_name)
df3=df2.withColumn("company_name",company_name_udf(col("company_name")))

df4=df3.withColumn("location",split(col("location"),","))

df5=df4.withColumns({"location_size":size(col("location")),\
                 "address":when( col("location_size")== 3 , col("location")[0] ),\
                 "city":when( col("location_size")== 3 , col("location")[1] )\
                       .when(col("location_size")== 2 , col("location")[0] ),\
                 "country":when( col("location_size")== 3 , col("location")[2] )\
                          .when( col("location_size")== 2 , col("location")[1] )\
                 }).drop("location","location_size")

df6=df5.withColumn("job_type",split(col("job_type"),' / ') )

df7=df6.withColumns({"work_type":col("job_type")[0],"workplace":col("job_type")[1]} )


df8=df7.drop("job_type")

df9 = df8.withColumn(
    "Yrs of Exp",
    when(col("Yrs of Exp").rlike(".*\\d.*"), col("Yrs of Exp")).otherwise(None)
)

df10=df9.dropDuplicates(["job_title","company_name","company_page","Experience Level","Yrs of Exp",\
                          "address","city","country","work_type","workplace","skills"])


df_skills=df10.select("id","skills")\
             .withColumn("skills", regexp_replace("skills", r"[\[\]']", ""))\
             .withColumn("skills", split(col("skills"), ",\s*"))\
             .withColumn("skills", explode(col("skills")))\
             .withColumnRenamed("id","job_id")\
             .withColumn("skills", trim(col("skills")))

window = Window.orderBy("job_id")

df_skills = df_skills.withColumn("id", row_number().over(window)).select("id","job_id","skills")

df11=df10.drop("skills")

df12=df11.fillna("UnKnown")

df13=df12.withColumnsRenamed({"Experience Level":"experience_level","Yrs of Exp":"yrs_of_exp"})

df14=df13.sort(col("id").asc())
 
df15 = df14.withColumn("job_title", regexp_replace(col("job_title"), '"', '')).withColumn("job_title",trim(col("job_title")))

df16=df15.select('id','job_title','work_type','workplace','company_name','company_page','experience_level',\
                 'yrs_of_exp', 'address','city','country')

df_skills=df_skills.fillna("UnKnown")

df16.write.option("header", True).mode("overwrite").csv("hdfs://namenode:8020/wuzzuf_output/Wuzzuf_data_transformed")
df_skills.write.option("header", True).mode("overwrite").csv("hdfs://namenode:8020/wuzzuf_output/skills")


##############################################################################3

