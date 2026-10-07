from pyspark.sql import SparkSession
import os
import shutil
from sqlalchemy import text
from sqlalchemy import create_engine



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

LANDING_DIR = "data/landing"
REJECTED_DIR = "data/rejected"

EXPECTED_COLS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn"
]

def detect_files():
    files = []

    for filename in os.listdir(LANDING_DIR):
        if filename.lower().endswith(".csv"):
            files.append(os.path.join(LANDING_DIR, filename))

    return files


def validate_schema(filepath):
    try:
        df = (
            spark.read
            .option("header", True)
            .option("inferSchema", False)
            .csv(filepath)
        )

        actual_cols = df.columns

        if actual_cols == EXPECTED_COLS:
            return True, ""

        missing_cols = [
            col for col in EXPECTED_COLS
            if col not in actual_cols
        ]

        extra_cols = [
            col for col in actual_cols
            if col not in EXPECTED_COLS
        ]

        reason = (
            f"Schema mismatch. "
            f"Missing columns: {missing_cols}. "
            f"Extra columns: {extra_cols}. "
            # f"Expected order: {EXPECTED_COLS}. "
            # f"Actual order: {actual_cols}"
        )

        return False, reason

    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def load_to_staging(filepath, engine=None):

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", False)
        .csv(filepath)
    )

    row_count = df.count()

    (
        df.write
        .mode("overwrite")
        .jdbc(
            url=JDBC_URL,
            table="stg_customer_raw",
            properties=JDBC_PROPERTIES
        )
    )

    return row_count


def reject_file(filepath):

    destination = os.path.join(
        REJECTED_DIR,
        os.path.basename(filepath)
    )

    shutil.move(filepath, destination)



def log_ingestion(filename, status, row_count, reason, engine):

    query = text("""
        INSERT INTO ingestion_log
        (filename, status, row_count, reason)
        VALUES
        (:filename, :status, :row_count, :reason)
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "filename": filename,
                "status": status,
                "row_count": row_count,
                "reason": reason
            }
        )

def process_landing(engine):

    files = detect_files()

    print(f"Detected {len(files)} file(s)")

    for filepath in files:

        filename = os.path.basename(filepath)

        print(f"\nProcessing: {filename}")

        # validating schema
      
        valid, reason = validate_schema(filepath)

        if not valid:

            print("REJECTED")
            print(reason)

            reject_file(filepath)

            log_ingestion(
                filename=filename,
                status="REJECTED",
                row_count=0,
                reason=reason,
                engine=engine
            )

            continue

        # Load to staging
       

        try:

            row_count = load_to_staging(
                filepath,
                engine
            )

            print(f"LOADED: {row_count} rows")


            # Log successful ingestion
          
            log_ingestion(
                filename=filename,
                status="LOADED",
                row_count=row_count,
                reason="",
                engine=engine
            )

            print("all done ......")

        except Exception as e:

            print("LOAD FAILED:", e)

            log_ingestion(
                filename=filename,
                status="REJECTED",
                row_count=0,
                reason=str(e),
                engine=engine
            )



process_landing(engine)

spark.stop()
# files = detect_files()

# print("Files detected:")
# for file in files:
#     print(file)

# valid, reason = validate_schema("data/landing/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# if valid:
#     print("Valid schema")
# else:
#     print("Invalid schema:", reason)


# row = load_to_staging("data/landing/WA_Fn-UseC_-Telco-Customer-Churn.csv")
# print("numbers of rows :", row)


