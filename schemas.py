from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import List, Optional
from enum import Enum

class LoanStatus(str, Enum):
    ACTIVE = "active"
    PAID = "paid"
    DEFAULTED = "defaulted"
    CANCELLED = "cancelled"

class RepaymentBase(BaseModel):
    amount: float
    payment_date: Optional[datetime] = None

class RepaymentCreate(RepaymentBase):
    loan_id: int

class Repayment(RepaymentBase):
    id: int
    loan_id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)

class LoanBase(BaseModel):
    principal: float
    interest_rate: float
    duration_days: int
    start_date: Optional[datetime] = None

class LoanCreate(LoanBase):
    customer_id: int

class Loan(LoanBase):
    id: int
    customer_id: int
    status: LoanStatus
    start_date: datetime

    # Calculated fields will be handled in a separate "Status" schema or by the service

    model_config = ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    # loans: List[Loan] = [] # Optional to avoid circular or heavy responses

    model_config = ConfigDict(from_attributes=True)

class LoanStatusDetail(BaseModel):
    loan_id: int
    customer_name: str
    principal: float
    interest_amount: float
    total_repayment: float
    daily_installment: float
    amount_paid: float
    remaining_balance: float
    status: LoanStatus
    next_payment_date: Optional[datetime]
    repayments: List[Repayment]
