from sqlalchemy import Column, Integer, String, Float,create_engine
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker,declarative_base
import pandas as pd

engine = create_engine("mysql+pymysql://root:root@localhost:3306/cris")

Base = declarative_base()

Session = sessionmaker(autocommit = False,
    autoflush= False,
    bind = engine     )

session = Session()

class StgCustomerRaw(Base):
    __tablename__ = "stg_customer_raw"

    customer_id = Column(String(20), primary_key=True)

    gender = Column(String(10), nullable=True)
    senior_citizen = Column(Integer, nullable=True)

    partner = Column(String(5), nullable=True)
    dependents = Column(String(5), nullable=True)

    tenure = Column(Integer, nullable=True)

    phone_service = Column(String(5), nullable=True)
    multiple_lines = Column(String(30), nullable=True)

    internet_service = Column(String(30), nullable=True)

    online_security = Column(String(30), nullable=True)
    online_backup = Column(String(30), nullable=True)
    device_protection = Column(String(30), nullable=True)
    tech_support = Column(String(30), nullable=True)

    streaming_t_v = Column(String(30), nullable=True)
    streaming_movies = Column(String(30), nullable=True)

    contract = Column(String(30), nullable=True)

    paperless_billing = Column(String(5), nullable=True)
    payment_method = Column(String(50), nullable=True)

    monthly_charges = Column(Float, nullable=True)

    # Keep as VARCHAR to preserve raw CSV values (including blanks)
    total_charges = Column(String(20), nullable=True)

    churn = Column(String(5), nullable=True)



Base.metadata.create_all(bind=engine)
print("tabel created ....")

df =pd.read_csv("phase2/sql1/clean_data_20260731_153340.csv")
# Rename columns to match your ORM/table names if necessary
print(df.columns)
df.drop([
    'high_charge_flag',
    'service_count',
    'is_long_term_customer',
    'has_streaming_bundle',
    'auto_pay_flag'
], axis=1, inplace=True)

print("dropped....")



# Rename columns to match your ORM/table names if necessary
df.columns = [
    "customer_id",
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "tenure",
    "phone_service",
    "multiple_lines",
    "internet_service",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_t_v",
    "streaming_movies",
    "contract",
    "paperless_billing",
    "payment_method",
    "monthly_charges",
    "total_charges",
    "churn"
]

# Insert into staging table
df.to_sql(
    name="stg_customer_raw",
    con=engine,
    if_exists="append",   # append rows
    index=False
)
