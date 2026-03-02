const express = require('express');
const { z } = require('zod');
const { sequelize, Customer, Loan, Repayment } = require('./models');
const { calculateLoanStatus } = require('./utils');

const app = express();
app.use(express.json());

// Validation Schemas
const customerSchema = z.object({
  name: z.string().min(1),
  phone: z.string().min(5),
  email: z.string().email().optional(),
  address: z.string().optional()
});

const loanSchema = z.object({
  customerId: z.number(),
  principal: z.number().positive(),
  interest_rate: z.number().nonnegative(),
  duration_days: z.number().int().positive()
});

const repaymentSchema = z.object({
  loanId: z.number(),
  amount: z.number().positive()
});

// Endpoints
app.post('/customers', async (req, res) => {
  try {
    const data = customerSchema.parse(req.body);
    const customer = await Customer.create(data);
    res.status(201).json(customer);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.get('/customers', async (req, res) => {
  const customers = await Customer.findAll();
  res.json(customers);
});

app.post('/loans', async (req, res) => {
  try {
    const data = loanSchema.parse(req.body);
    const customer = await Customer.findByPk(data.customerId);
    if (!customer) return res.status(404).json({ error: 'Customer not found' });

    const loan = await Loan.create({
      principal: data.principal,
      interest_rate: data.interest_rate,
      duration_days: data.duration_days,
      CustomerId: data.customerId
    });
    res.status(201).json(loan);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.get('/loans/:id/status', async (req, res) => {
  const loan = await Loan.findByPk(req.params.id);
  if (!loan) return res.status(404).json({ error: 'Loan not found' });

  const status = await calculateLoanStatus(loan);
  res.json(status);
});

app.post('/repayments', async (req, res) => {
  try {
    const data = repaymentSchema.parse(req.body);
    const loan = await Loan.findByPk(data.loanId);
    if (!loan) return res.status(404).json({ error: 'Loan not found' });
    if (loan.status === 'paid') return res.status(400).json({ error: 'Loan already paid' });

    const repayment = await Repayment.create({
      amount: data.amount,
      LoanId: data.loanId
    });

    // Check if fully paid
    const status = await calculateLoanStatus(loan);
    if (status.remainingBalance <= 0) {
      loan.status = 'paid';
      await loan.save();
    }

    res.status(201).json(repayment);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = app;
