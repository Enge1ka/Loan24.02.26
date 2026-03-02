# Loan Management System (JavaScript/Express)

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
- Node.js
- Express
- Sequelize (SQLite)
- Zod (Validation)
- Jest & Supertest (Testing)

## Getting Started
1. Install dependencies:
   ```bash
   npm install
   ```
2. Run the application:
   ```bash
   node index.js
   ```

## Testing
```bash
npm test
```
