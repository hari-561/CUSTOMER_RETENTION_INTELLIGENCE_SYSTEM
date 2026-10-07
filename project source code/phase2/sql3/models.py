from sqlalchemy import Column, Integer, Float, String, DECIMAL,Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from database import Base


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




class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(20), primary_key=True)
    gender = Column(String(10))
    senior_citizen = Column(Integer, nullable=False)
    partner = Column(Integer, nullable=False)
    dependent = Column(Integer, nullable=False)

    accounts = relationship(
        "FactCustomerAccount",
        back_populates="customer"
    )


class DimContract(Base):
    __tablename__ = "dim_contract"

    contract_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    contract_name = Column(
        String(20),
        unique=True,
        nullable=False
    )

    accounts = relationship(
        "FactCustomerAccount",
        back_populates="contract"
    )

class DimPayment(Base):
    __tablename__ = "dim_payment"

    payment_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    payment_method = Column(
        String(50),
        unique=True,
        nullable=False
    )

    accounts = relationship(
        "FactCustomerAccount",
        back_populates="payment"
    )



class FactCustomerAccount(Base):
    __tablename__ = "fact_customer_account"

    fact_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id")
    )

    contract_key = Column(
        Integer,
        ForeignKey("dim_contract.contract_key")
    )

    payment_key = Column(
        Integer,
        ForeignKey("dim_payment.payment_key")
    )

    tenure = Column(Integer)

    monthly_charges = Column(DECIMAL(10, 2))

    total_charges = Column(DECIMAL(10, 2))

    churn = Column(Boolean)

    customer = relationship(
        "Customer",
        back_populates="accounts"
    )

    contract = relationship(
        "DimContract",
        back_populates="accounts"
    )

    payment = relationship(
        "DimPayment",
        back_populates="accounts"
    )


class customerMLfeatures(Base):
    __tablename__ = "customer_ml_features"

    customer_id = Column(String(20), primary_key=True)
    gender = Column(String(10))
    senior_citizen = Column(Integer, nullable=False)
    partner = Column(Integer, nullable=False)
    dependent = Column(Integer, nullable=False)
    contract_name = Column(String(20))
    payment_method = Column(String(50))
    tenure = Column(Integer)
    monthly_charges = Column(DECIMAL(10, 2))  
    total_charges = Column(DECIMAL(10, 2))
    services_count = Column(Integer)
    high_charge_flag = Column(Integer)
    is_long_term_contract = Column(Integer)
    auto_pay_flag = Column(Integer)
    churn = Column(Integer, nullable=False)



