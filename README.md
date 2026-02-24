# Loan Management System

A system to manage customers, loans, and daily repayments.

## Features
- Manage Customers (CRUD)
- Manage Loans (Create, View, Status)
- Manage Daily Repayments (Record, View)
- Automatic calculation of:
    - Total repayment amount
    - Daily repayment requirements
    - Current balance
    - Next due date

## Tech Stack
- FastAPI (API)
- SQLAlchemy with SQLite (Database)
- Pydantic (Data Validation)

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
3. Visit `http://127.0.0.1:8000/docs` for API documentation.
