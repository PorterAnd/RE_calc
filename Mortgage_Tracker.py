import streamlit as st
import pandas as pd
from Mortgage_Calculations import MortgageCalculator

st.title("🏠 Mortgage Calculator")

# User Inputs
house_price = st.number_input("Home Price ($)", value=300000, step=10000, format="%i")
down_payment_pct = st.number_input("Down Payment (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.5, format="%.1f")

term_option = st.selectbox("Mortgage Term", options=["15 years", "30 years", "Other"])
if term_option == "15 years":
    mortgage_term_years = 15
elif term_option == "30 years":
    mortgage_term_years = 30
else:
    mortgage_term_years = st.number_input("Custom mortgage term (years)", min_value=1, max_value=50, value=20)

interest_rate = st.number_input("Interest Rate (% Annual)", value=6.5, step=0.1, format="%.2f")

# Mortgage calculation
calculator = MortgageCalculator(house_price, down_payment_pct, mortgage_term_years, interest_rate)
monthly_payment = calculator.monthly_payment

st.metric("Mortgage Payment / Month", f"${monthly_payment:,.2f}")

# Save mortgage payment to session state
st.session_state['monthly_mortgage_payment'] = monthly_payment

# Amortization Table
st.subheader("📊 Amortization Schedule")

amortization_df = calculator.generate_amortization_schedule()

st.dataframe(
    amortization_df.style.format({
        "Month": "{:.0f}",
        "Payment": "${:,.2f}",
        "Principal Paid": "${:,.2f}",
        "Interest Paid": "${:,.2f}",
        "Loan Amount Paid": "${:,.2f}",
        "Remaining Balance": "${:,.2f}",
    }),
    use_container_width=True
)

# Optional line chart
if st.checkbox("📈 Show Principal vs. Interest Over Time"):
    chart_df = amortization_df[["Month", "Principal Paid", "Interest Paid"]]
    st.line_chart(chart_df.set_index("Month"))
