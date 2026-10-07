from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from functools import reduce
import os


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

# engine = create_engine(
#     "mysql+pymysql://root:root@localhost/python_prac"
# )


FEATURE_COLUMNS = [
    "tenure_bucket",
    "high_charge_flag",
    "service_count",
    "is_long_term_customer",
    "has_streaming_bundle",
    "auto_pay_flag"
]

def build_features(engine = None):

    print("\n===================================")
    print("Building ML Features")
    print("===================================")

    # ==========================================
    # Read cleaned data
    # ==========================================

    cleaned_df = (
        spark.read
        .jdbc(
            url=JDBC_URL,
            table="cleaned_customers",
            properties=JDBC_PROPERTIES
        )
    )

    cleaned_count = cleaned_df.count()

    print(
        f"Rows in cleaned_customers: "
        f"{cleaned_count}"
    )

    # ==========================================
    # Feature 1
    # tenure_bucket
    # ==========================================

    cleaned_df = cleaned_df.withColumn(
        "tenure_bucket",
        when(
            (cleaned_df.tenure >= 0) &
            (cleaned_df.tenure <= 12),
            "0-12"
        )
        .when(
            (cleaned_df.tenure > 12) &
            (cleaned_df.tenure <= 24),
            "12-24"
        )
        .when(
            (cleaned_df.tenure > 24) &
            (cleaned_df.tenure <= 48),
            "24-48"
        )
        .when(
            (cleaned_df.tenure > 48) &
            (cleaned_df.tenure <= 72),
            "48-72"
        )
    )


    cleaned_df.select( col("customer_id"),
                      col("tenure"), 
                      col("tenure_bucket") ) \
                      .where (col("tenure_bucket").isNull()).show()

    # ==========================================
    # Feature 2
    # high_charge_flag
    # ==========================================

    median_monthly_charges = cleaned_df.select(
        expr(
            "percentile_approx(monthly_charges, 0.5)"
        ).alias("median")
    ).collect()[0]["median"]

    print(
        f"Median monthly charges: "
        f"{median_monthly_charges}"
    )

    cleaned_df = cleaned_df.withColumn(
        "high_charge_flag",
        when(
            cleaned_df.monthly_charges >
            median_monthly_charges,
            1
        ).otherwise(0)
    )

    # ==========================================
    # Feature 3
    # service_count
    # ==========================================



    service_columns = [
        "online_security",
        "online_backup",
        "device_protection",
        "tech_support",
        "streaming_tv",
        "streaming_movies"
    ]



    service_count_expr = reduce(
        lambda x, y: x + y,
        [when(col(c) == "Yes", 1).otherwise(0) for c in service_columns]
    )

    cleaned_df = cleaned_df.withColumn(
        "service_count",
        service_count_expr
    )


    # ==========================================
    # Feature 4
    # is_long_term_customer
    # ==========================================

    cleaned_df = cleaned_df.withColumn(
        "is_long_term_customer",
        when(
            cleaned_df.tenure >= 24,
            1
        ).otherwise(0)
    )

    # ==========================================
    # Feature 5
    # has_streaming_bundle
    # ==========================================

    cleaned_df = cleaned_df.withColumn(
        "has_streaming_bundle",
        when(
            (cleaned_df.streaming_tv == "Yes") &
            (cleaned_df.streaming_movies == "Yes"),
            1
        ).otherwise(0)
    )

    # ==========================================
    # Feature 6
    # auto_pay_flag
    # ==========================================

    cleaned_df = cleaned_df.withColumn(
        "auto_pay_flag",
        when(
            lower(
                cleaned_df.payment_method
            ).contains("automatic"),
            1
        ).otherwise(0)
    )

    # ==========================================
    # 198. Row count validation
    # ==========================================

    feature_count = cleaned_df.count()

    assert feature_count == cleaned_count, (
        f"Row count mismatch: "
        f"cleaned_customers={cleaned_count}, "
        f"customer_ml_features={feature_count}"
    )

    print(
        f"PASS - Row count check: "
        f"{feature_count} == {cleaned_count}"
    )

    # ==========================================
    # Write feature table
    # ==========================================

    (
        cleaned_df.write \
        .mode("overwrite") \
        .jdbc(
            url=JDBC_URL,
            table="customer_ml_features",
            properties=JDBC_PROPERTIES
        )
    )

    print(
        "customer_ml_features table populated"
    )

    return cleaned_df



def validate_feature_schema(df):

    print("\n===================================")
    print("Feature Schema Validation")
    print("===================================")

    # Check columns exist
    missing_columns = [
        col
        for col in FEATURE_COLUMNS
        if col not in df.columns
    ]

    assert not missing_columns, (
        f"Missing feature columns: "
        f"{missing_columns}"
    )

    print(
        "PASS - All 6 feature columns present"
    )

    # Check NULLs
    for col in FEATURE_COLUMNS:

        null_count = df.filter(
            df[col].isNull()
        ).count()

        if null_count == 0:

            print(
                f"PASS - {col}: "
                f"{null_count} NULLs"
            )

        else:

            print(
                f"FAIL - {col}: "
                f"{null_count} NULLs"
            )

        assert null_count == 0, (
            f"{col} contains "
            f"{null_count} NULL values"
        )


features_df = build_features()

validate_feature_schema(features_df)

features_df.select(
    "customer_id",
    "tenure",
    "monthly_charges",
    "payment_method",
    "tenure_bucket",
    "high_charge_flag",
    "service_count",
    "is_long_term_customer",
    "has_streaming_bundle",
    "auto_pay_flag",
    "churn"
).show(3, truncate=False)