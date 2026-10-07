from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType
)
import pandas as pd
from pyspark.sql.functions import *
import os

os.environ["HADOOP_HOME"] = r"C:\Users\harikumar.g\OneDrive - Prodapt Solutions Private Limited\Desktop\training\K Valuent\day22\hadoop"
os.environ["PATH"] = os.environ["PATH"] + r";C:\Users\harikumar.g\OneDrive - Prodapt Solutions Private Limited\Desktop\training\K Valuent\day22\hadoop\bin"
 

spark = (
    SparkSession.builder
    .appName("CustomerChurnSparkAnalysis")
    .master("local[2]")
    .config("spark.driver.memory", "4g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")



schema = StructType([
    StructField("customerID", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("SeniorCitizen", IntegerType(), True),
    StructField("Partner", StringType(), True),
    StructField("Dependents", StringType(), True),
    StructField("tenure", IntegerType(), True),
    StructField("PhoneService", StringType(), True),
    StructField("MultipleLines", StringType(), True),
    StructField("InternetService", StringType(), True),
    StructField("OnlineSecurity", StringType(), True),
    StructField("OnlineBackup", StringType(), True),
    StructField("DeviceProtection", StringType(), True),
    StructField("TechSupport", StringType(), True),
    StructField("StreamingTV", StringType(), True),
    StructField("StreamingMovies", StringType(), True),
    StructField("Contract", StringType(), True),
    StructField("PaperlessBilling", StringType(), True),
    StructField("PaymentMethod", StringType(), True),
    StructField("MonthlyCharges", DoubleType(), True),

    # IMPORTANT: StringType initially
    StructField("TotalCharges", StringType(), True),

    StructField("Churn", StringType(), True)
])

CSV_PATH = "data/landing/WA_Fn-UseC_-Telco-Customer-Churn.csv"   

df = (
    spark.read
    .option("header", True)
    .schema(schema)
    .csv(CSV_PATH)
)

print("Spark Schema:")
df.printSchema()

pandasdf = pd.read_csv(CSV_PATH)
print("Pandas Schema")
print(pandasdf.info())

df = df.withColumn(
    "TotalCharges",
     regexp_replace(
        col("TotalCharges"),
        r"^\s*$",
        ""
    ).cast("double")
)


df = df.withColumn(
    "churn",
    when(
        col("churn") == "Yes",
        1
    ).otherwise(0)
)


df.select("churn").show(5)



contract_summary = (
    df
    .groupBy("Contract")
    .agg(
        count("*").alias("customer_count"),
        avg("churn").alias("churn_rate")
    )
    .orderBy(
        col("churn_rate").desc()
    )
)

contract_summary.show()


internet_summary = (
    df
    .groupBy("InternetService")
    .agg(
        avg("MonthlyCharges").alias(
            "avg_monthly_charges"
        ),
        avg("churn").alias(
            "churn_rate"
        )
    )
    .orderBy(
        col("churn_rate").desc()
    )
)

internet_summary.show()


OUTPUT_PATH = "data/spark_output/contract_summary"

(
    contract_summary
    .write
    .mode("overwrite")
    .partitionBy("Contract")
    .parquet(OUTPUT_PATH)
)


parquet_df = spark.read.parquet(
    OUTPUT_PATH
)

print("\nParquet schema:")

parquet_df.printSchema()

print(
    f"Parquet row count: "
    f"{parquet_df.count()}"
)

parquet_df.show()

assert parquet_df.count() == contract_summary.count()

print(
    "PASS - Parquet round-trip is clean"
)
