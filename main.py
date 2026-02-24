from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud, database
from database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Management System")

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_phone(db, phone=customer.phone)
    if db_customer:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.post("/loans/", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    db_customer = crud.get_customer(db, customer_id=loan.customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.create_loan(db=db, loan=loan)

@app.get("/loans/{loan_id}/status", response_model=schemas.LoanStatusDetail)
def get_loan_status(loan_id: int, db: Session = Depends(get_db)):
    status = crud.get_loan_status(db, loan_id=loan_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return status

@app.post("/repayments/", response_model=schemas.Repayment)
def create_repayment(repayment: schemas.RepaymentCreate, db: Session = Depends(get_db)):
    # Check if loan exists
    db_loan = crud.get_loan(db, loan_id=repayment.loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if db_loan.status == models.LoanStatus.PAID:
        raise HTTPException(status_code=400, detail="Loan already fully paid")
    return crud.create_repayment(db=db, repayment=repayment)

@app.get("/loans/", response_model=List[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
