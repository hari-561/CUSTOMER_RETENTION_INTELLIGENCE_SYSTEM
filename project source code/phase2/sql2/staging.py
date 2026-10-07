from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float
)
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class StagingCustomer(Base):
    __tablename__ = "staging_customer"

    customerID = Column(String(20), primary_key=True)

    gender = Column(String(10))
    SeniorCitizen = Column(Integer)

    Partner = Column(String(5))
    Dependents = Column(String(5))

    tenure = Column(Integer)

    PhoneService = Column(String(5))
    MultipleLines = Column(String(25))

    InternetService = Column(String(20))

    OnlineSecurity = Column(String(25))
    OnlineBackup = Column(String(25))
    DeviceProtection = Column(String(25))
    TechSupport = Column(String(25))

    StreamingTV = Column(String(25))
    StreamingMovies = Column(String(25))

    Contract = Column(String(25))

    PaperlessBilling = Column(String(5))

    PaymentMethod = Column(String(50))

    MonthlyCharges = Column(Float)

    # Keep as String because your dataframe has object/string dtype
    TotalCharges = Column(String(20))

    Churn = Column(String(5))


engine = create_engine(
    "mysql+pymysql://root:root@localhost/telecom_chrun"
)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



