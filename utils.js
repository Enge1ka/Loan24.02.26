const calculateLoanStatus = async (loan) => {
  const repayments = await loan.getRepayments();
  const totalPaid = repayments.reduce((sum, r) => sum + r.amount, 0);

  const interestAmount = loan.principal * (loan.interest_rate / 100);
  const totalRepayment = loan.principal + interestAmount;

  const dailyInstallment = loan.duration_days > 0 ? totalRepayment / loan.duration_days : 0;
  const remainingBalance = totalRepayment - totalPaid;

  // Next payment date: start_date + (number of repayments + 1) days
  const startDate = new Date(loan.start_date);
  const nextPaymentDate = new Date(startDate);
  nextPaymentDate.setDate(startDate.getDate() + repayments.length + 1);

  return {
    loanId: loan.id,
    principal: loan.principal,
    interestAmount,
    totalRepayment,
    dailyInstallment,
    amountPaid: totalPaid,
    remainingBalance,
    status: loan.status,
    nextPaymentDate,
    repayments
  };
};

module.exports = {
  calculateLoanStatus
};
