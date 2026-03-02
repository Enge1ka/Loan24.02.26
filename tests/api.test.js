const request = require('supertest');
const app = require('../app');
const { sequelize } = require('../models');

beforeAll(async () => {
  await sequelize.sync({ force: true });
});

afterAll(async () => {
  await sequelize.close();
});

describe('Loan Management API', () => {
  it('should create a customer', async () => {
    const res = await request(app)
      .post('/customers')
      .send({
        name: 'John Doe',
        phone: '1234567890',
        email: 'john@example.com'
      });
    expect(res.statusCode).toEqual(201);
    expect(res.body.name).toEqual('John Doe');
  });

  it('should create a loan', async () => {
    const res = await request(app)
      .post('/loans')
      .send({
        customerId: 1,
        principal: 1000,
        interest_rate: 10,
        duration_days: 10
      });
    expect(res.statusCode).toEqual(201);
    expect(res.body.principal).toEqual(1000);
  });

  it('should calculate loan status correctly', async () => {
    const res = await request(app).get('/loans/1/status');
    expect(res.statusCode).toEqual(200);
    expect(res.body.totalRepayment).toEqual(1100);
    expect(res.body.dailyInstallment).toEqual(110);
    expect(res.body.remainingBalance).toEqual(1100);
  });

  it('should record a repayment and update balance', async () => {
    await request(app)
      .post('/repayments')
      .send({
        loanId: 1,
        amount: 220
      });

    const res = await request(app).get('/loans/1/status');
    expect(res.body.amountPaid).toEqual(220);
    expect(res.body.remainingBalance).toEqual(880);
    expect(res.body.status).toEqual('active');
  });

  it('should mark loan as paid when fully paid', async () => {
    await request(app)
      .post('/repayments')
      .send({
        loanId: 1,
        amount: 880
      });

    const res = await request(app).get('/loans/1/status');
    expect(res.body.remainingBalance).toEqual(0);
    expect(res.body.status).toEqual('paid');
  });
});
