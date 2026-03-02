const { Sequelize, DataTypes } = require('sequelize');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './loan_management.db',
  logging: false
});

const Customer = sequelize.define('Customer', {
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  phone: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  email: {
    type: DataTypes.STRING,
    allowNull: true
  },
  address: {
    type: DataTypes.TEXT,
    allowNull: true
  }
});

const Loan = sequelize.define('Loan', {
  principal: {
    type: DataTypes.FLOAT,
    allowNull: false
  },
  interest_rate: {
    type: DataTypes.FLOAT,
    allowNull: false
  },
  duration_days: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('active', 'paid', 'defaulted', 'cancelled'),
    defaultValue: 'active'
  },
  start_date: {
    type: DataTypes.DATE,
    defaultValue: Sequelize.NOW
  }
});

const Repayment = sequelize.define('Repayment', {
  amount: {
    type: DataTypes.FLOAT,
    allowNull: false
  },
  payment_date: {
    type: DataTypes.DATE,
    defaultValue: Sequelize.NOW
  }
});

Customer.hasMany(Loan);
Loan.belongsTo(Customer);

Loan.hasMany(Repayment);
Repayment.belongsTo(Loan);

module.exports = {
  sequelize,
  Customer,
  Loan,
  Repayment
};
