from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,DateTime
)
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

from datetime import datetime
import pandas as pd
from staging import session, StagingCustomer

Base = declarative_base()
df = pd.read_csv("C:/Users/harikumar.g/OneDrive - Prodapt Solutions Private Limited/Desktop/training/K Valuent/assign/WA_Fn-UseC_-Telco-Customer-Churn.csv")

class IngestionLog(Base):
    __tablename__ = "ingestion_log"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100))
    load_time = Column(DateTime)
    row_count = Column(Integer)
    status = Column(String(20))


log = IngestionLog(
    table_name="staging_customer",
    load_time=datetime.now(),
    row_count=len(df),
    status="SUCCESS"
)

session.add(log)
session.commit()