import pandas as pd

class MortgageCalculator:
    def __init__(self, house_price, down_payment_pct, mortgage_term_years, annual_interest_rate):
        self.house_price = house_price
        self.down_payment_pct = down_payment_pct
        self.mortgage_term_years = mortgage_term_years
        self.annual_interest_rate = annual_interest_rate

        self.loan_amount = self._calculate_loan_amount()
        self.monthly_interest_rate = self._calculate_monthly_interest_rate()
        self.total_payments = self.mortgage_term_years * 12
        self.monthly_payment = self._calculate_monthly_payment()

    def _calculate_loan_amount(self):
        return self.house_price * (1 - self.down_payment_pct / 100)

    def _calculate_monthly_interest_rate(self):
        return (self.annual_interest_rate / 100) / 12

    def _calculate_monthly_payment(self):
        r = self.monthly_interest_rate
        n = self.total_payments
        p = self.loan_amount
        return p * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    def generate_amortization_schedule(self):
        schedule = []
        balance = self.loan_amount
        cumulative_principal = 0

        for month in range(1, self.total_payments + 1):
            interest = balance * self.monthly_interest_rate
            principal = self.monthly_payment - interest
            ending_balance = balance - principal
            cumulative_principal += principal

            schedule.append({
                "Month": month,
                "Payment": round(self.monthly_payment, 2),
                "Principal Paid": round(principal, 2),
                "Interest Paid": round(interest, 2),
                "Loan Amount Paid": round(cumulative_principal, 2),
                "Remaining Balance": round(ending_balance, 2)
            })

            balance = ending_balance

        return pd.DataFrame(schedule)
