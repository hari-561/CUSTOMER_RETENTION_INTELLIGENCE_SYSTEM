from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,Boolean,Float,ForeignKey,engine
from sqlalchemy.orm import create_session,declarative_base,relationship




# ----------------------------
# Customers (Identity)
# ----------------------------
class Customer(BaseModel):
    __tablename__ = "customers"

    customer_id = Column(String(20), primary_key=True)
    gender = Column(String(10), nullable=False)
    senior_citizen = Column(Boolean, nullable=False)
    partner = Column(Boolean, nullable=False)
    dependents = Column(Boolean, nullable=False)

    contract = relationship("Contract", back_populates="customer", uselist=False)
    service = relationship("Service", back_populates="customer", uselist=False)
    billing = relationship("Billing", back_populates="customer", uselist=False)
    status = relationship("CustomerStatus", back_populates="customer", uselist=False)


# ----------------------------
# Contract (Subscription Terms)
# ----------------------------
class Contract(BaseModel):
    __tablename__ = "contracts"

    contract_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False,
        unique=True
    )

    contract = Column(String(30), nullable=False)
    tenure = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="contract")


# ----------------------------
# Services
# ----------------------------
class Service(BaseModel):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False,
        unique=True
    )

    phone_service = Column(Boolean)
    multiple_lines = Column(String(30))
    internet_service = Column(String(30))
    online_security = Column(String(30))
    online_backup = Column(String(30))
    device_protection = Column(String(30))
    tech_support = Column(String(30))
    streaming_t_v = Column(String(30))
    streaming_movies = Column(String(30))

    customer = relationship("Customer", back_populates="service")


# ----------------------------
# Billing
# ----------------------------
class Billing(BaseModel):
    __tablename__ = "billing"

    billing_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False,
        unique=True
    )

    paperless_billing = Column(Boolean)
    payment_method = Column(String(50))
    monthly_charges = Column(Float)
    total_charges = Column(Float)

    customer = relationship("Customer", back_populates="billing")


# ----------------------------
# Customer Status
# ----------------------------
class CustomerStatus(BaseModel):
    __tablename__ = "customer_status"

    status_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False,
        unique=True
    )

    churn = Column(Boolean)

    customer = relationship("Customer", back_populates="status")