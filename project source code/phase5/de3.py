import os
import sys

sys.path.append(os.path.abspath(".."))

from phase1.cleanermodel import customer_cleaner
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number


from sqlalchemy import create_engine,text


os.environ["HADOOP_HOME"] = r"C:\Users\harikumar.g\OneDrive - Prodapt Solutions Private Limited\Desktop\training\K Valuent\day22\hadoop"
os.environ["PATH"] = os.environ["PATH"] + r";C:\Users\harikumar.g\OneDrive - Prodapt Solutions Private Limited\Desktop\training\K Valuent\day22\hadoop\bin"
 

spark = (
    SparkSession.builder
    .appName("CustomerChurnIngestion")
    .config("spark.jars", r"C:\Users\harikumar.g\OneDrive - Prodapt Solutions Private Limited\Desktop\training\K Valuent\day22\mysql-connector-j-26.7.0\mysql-connector-j-26.7.0.jar") \
    .getOrCreate()
)
 
JDBC_URL = "jdbc:mysql://localhost:3306/python_prac"

JDBC_PROPERTIES = {
    "user": "root",
    "password": "root",
    "driver": "com.mysql.cj.jdbc.Driver"
}

engine = create_engine(
    "mysql+pymysql://root:root@localhost/python_prac"
)


def read_staging():

    df = (
        spark.read
        .jdbc(
            url=JDBC_URL,
            table="stg_customer_raw",
            properties=JDBC_PROPERTIES
        )
    )

    return df


def clean_staging(engine = None):

    print("\n==============================")
    print("Cleaning staging data")
    print("==============================")

    # 1. Read staging table
    staging_df = (
        spark.read
        .jdbc(
            url=JDBC_URL,
            table="stg_customer_raw",
            properties=JDBC_PROPERTIES
        )
    )

    staging_count = staging_df.count()

    print(f"Rows in stg_customer_raw: {staging_count}")

    # 2. Convert Spark DataFrame to Pandas
    pandas_df = staging_df.toPandas()

    print("cleaning started ...........")
    # 3. Run your existing CustomerCleaner
    cleaner = customer_cleaner(pandas_df)

    cleaned_pandas_df = cleaner.clean()
    print("info of cleaned data:  ")
    print(cleaned_pandas_df.info())

    # 4. Convert Pandas back to Spark
    cleaned_spark_df = spark.createDataFrame(
        cleaned_pandas_df
    )

    cleaned_count = cleaned_spark_df.count()

    print(f"Rows after cleaning: {cleaned_count}")

    assert cleaned_count == staging_count, (
        f"Row count mismatch: "
        f"staging={staging_count}, "
        f"cleaned={cleaned_count}"
    )

    print(
        f"PASS - Row count check: "
        f"{staging_count} == {cleaned_count}"
    )

    # 5. Write to cleaned_customers
    (
        cleaned_spark_df.write
        .mode("overwrite")
        .jdbc(
            url=JDBC_URL,
            table="cleaned_customers",
            properties=JDBC_PROPERTIES
        )
    )

    print("cleaned_customers table populated")

    return cleaned_spark_df


def run_quality_checks(df):

    print("\n==============================")
    print("DATA QUALITY REPORT")
    print("==============================")

    # --------------------------------
    # Check 1: customer_id NULLs
    # --------------------------------

    null_customer_id = df.filter(
        df["customer_id"].isNull()
    ).count()

    if null_customer_id == 0:
        print(
            f"PASS - customer_id NULL check: "
            f"{null_customer_id}"
        )
    else:
        print(
            f"FAIL - customer_id NULL check: "
            f"{null_customer_id}"
        )

    # --------------------------------
    # Check 2: monthly_charges NULLs
    # --------------------------------

    null_monthly_charges = df.filter(
        df["monthly_charges"].isNull()
    ).count()

    if null_monthly_charges == 0:
        print(
            f"PASS - monthly_charges NULL check: "
            f"{null_monthly_charges}"
        )
    else:
        print(
            f"FAIL - monthly_charges NULL check: "
            f"{null_monthly_charges}"
        )

    # --------------------------------
    # Check 3: churn values
    # --------------------------------

    invalid_churn = df.filter(
        ~df["churn"].isin(0, 1)
    ).count()

    if invalid_churn == 0:
        print(
            f"PASS - churn values check: "
            f"{invalid_churn} invalid values"
        )
    else:
        print(
            f"FAIL - churn values check: "
            f"{invalid_churn} invalid values"
        )

    # --------------------------------
    # Assertions
    # --------------------------------

    assert null_customer_id == 0, (
        f"customer_id contains "
        f"{null_customer_id} NULL values"
    )

    assert null_monthly_charges == 0, (
        f"monthly_charges contains "
        f"{null_monthly_charges} NULL values"
    )

    assert invalid_churn == 0, (
        f"churn contains "
        f"{invalid_churn} invalid values"
    )


def build_curated_tables(engine = None):

    # Read cleaned data
    
    cleaned_df = (
        spark.read
        .jdbc(
            url=JDBC_URL,
            table="cleaned_customers",
            properties=JDBC_PROPERTIES
        )
    )

    # dim_contract
    contract_window = Window.orderBy("contract_name")

    dim_contract = (
        cleaned_df
        .select("contract")
        .distinct()
        .withColumnRenamed(
            "contract",
            "contract_name"
        )
        .withColumn(
            "contract_id",
            row_number().over(contract_window)
        )
        .select(
            "contract_id",
            "contract_name"
        )
    )

    dim_contract.write \
        .mode("overwrite") \
        .jdbc(
            url=JDBC_URL,
            table="dim_contract",
            properties=JDBC_PROPERTIES
        )

    # ==========================================
    # dim_payment
    # ==========================================

    payment_window = Window.orderBy("payment_method_name")

    dim_payment = (
        cleaned_df
        .select("payment_method")
        .distinct()
        .withColumnRenamed(
            "payment_method",
            "payment_method_name"
        )
        .withColumn(
            "payment_id",
            row_number().over(payment_window)
        )
        .select(
            "payment_id",
            "payment_method_name"
        )
    )

    dim_payment.write \
        .mode("overwrite") \
        .jdbc(
            url=JDBC_URL,
            table="dim_payment",
            properties=JDBC_PROPERTIES
        )

    # ==========================================
    # customers
    # ==========================================

    customers = cleaned_df.select(
        "customer_id",
        "gender",
        "senior_citizen",
        "partner",
        "dependents"
    )

    customers.write \
        .mode("overwrite") \
        .jdbc(
            url=JDBC_URL,
            table="customers",
            properties=JDBC_PROPERTIES
        )

    # ==========================================
    # fact_customer_account
    # ==========================================

    fact = (
        cleaned_df
        .join(
            dim_contract,
            cleaned_df.contract ==
            dim_contract.contract_name,
            "left"
        )
        .join(
            dim_payment,
            cleaned_df.payment_method ==
            dim_payment.payment_method_name,
            "left"
        )
    )

    fact_customer_account = fact.select(
        "customer_id",
        "contract_id",
        "payment_id",
        "tenure",
        "phone_service",
        "monthly_charges",
        "total_charges",
        "churn"
    )

    fact_customer_account.write \
        .mode("overwrite") \
        .jdbc(
            url=JDBC_URL,
            table="fact_customer_account",
            properties=JDBC_PROPERTIES
        )

    print("dim_contract populated")
    print("dim_payment populated")
    print("customers populated")
    print("fact_customer_account populated")


df = clean_staging()
run_quality_checks(df) 

# build_curated_tables()
# print("dome......")

spark.stop()

