from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, UTC
import enum

Base = declarative_base()

class LoanStatus(enum.Enum):
    ACTIVE = "active"
    PAID = "paid"
    DEFAULTED = "defaulted"
    CANCELLED = "cancelled"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    loans = relationship("Loan", back_populates="customer")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    principal = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False) # Total interest percentage
    duration_days = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=lambda: datetime.now(UTC))
    status = Column(SQLEnum(LoanStatus), default=LoanStatus.ACTIVE)

    customer = relationship("Customer", back_populates="loans")
    repayments = relationship("Repayment", back_populates="loan")

class Repayment(Base):
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=lambda: datetime.now(UTC))

    loan = relationship("Loan", back_populates="repayments")
