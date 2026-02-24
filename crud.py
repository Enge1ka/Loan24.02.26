from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime, timedelta, UTC

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_phone(db: Session, phone: str):
    return db.query(models.Customer).filter(models.Customer.phone == phone).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).offset(skip).limit(limit).all()

def create_repayment(db: Session, repayment: schemas.RepaymentCreate):
    db_repayment = models.Repayment(**repayment.model_dump())
    db.add(db_repayment)
    db.commit()
    db.refresh(db_repayment)

    # Check if loan is fully paid
    loan = get_loan(db, repayment.loan_id)
    status_detail = get_loan_status(db, loan.id)
    if status_detail.remaining_balance <= 0:
        loan.status = models.LoanStatus.PAID
        db.commit()
        db.refresh(loan)

    return db_repayment

def get_loan_status(db: Session, loan_id: int) -> schemas.LoanStatusDetail:
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        return None

    total_paid = sum(r.amount for r in loan.repayments)

    # Interest amount calculation: Principal * (interest_rate / 100)
    interest_amount = loan.principal * (loan.interest_rate / 100)
    total_repayment = loan.principal + interest_amount

    daily_installment = total_repayment / loan.duration_days if loan.duration_days > 0 else 0
    remaining_balance = total_repayment - total_paid

    # Calculate next payment date
    # Simple logic: start_date + number of repayments already made + 1 day
    # Or start_date + days passed since start if daily?
    # Let's say it's daily starting from start_date + 1 day

    # Ensure loan.start_date is timezone aware if we are using datetime.now(UTC)
    start_date = loan.start_date
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=UTC)

    days_passed = (datetime.now(UTC) - start_date).days
    next_payment_date = start_date + timedelta(days=len(loan.repayments) + 1)

    return schemas.LoanStatusDetail(
        loan_id=loan.id,
        customer_name=loan.customer.name,
        principal=loan.principal,
        interest_amount=interest_amount,
        total_repayment=total_repayment,
        daily_installment=daily_installment,
        amount_paid=total_paid,
        remaining_balance=remaining_balance,
        status=loan.status.value,
        next_payment_date=next_payment_date,
        repayments=[schemas.Repayment.model_validate(r) for r in loan.repayments]
    )
