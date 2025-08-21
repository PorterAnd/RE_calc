import streamlit as st
from Mortgage_Calculations import MortgageCalculator
import pandas as pd

st.title("🏠 Mortgage Calculator - Scenario Comparison")

# Initialize scenarios list in session_state
if "scenarios" not in st.session_state:
    st.session_state.scenarios = []

def add_scenario():
    # Add a new scenario with default values
    st.session_state.scenarios.append({
        "house_price": 300000,
        "down_payment_pct": 20.0,
        "mortgage_term_years": 30,
        "interest_rate": 6.5
    })

# Button to add a new scenario
if st.button("Add Scenario"):
    add_scenario()

# If no scenarios yet, add one by default
if not st.session_state.scenarios:
    add_scenario()

# Container to hold all scenario inputs and results
comparison_results = []

for i, scenario in enumerate(st.session_state.scenarios):
    st.markdown(f"### Scenario {i + 1}")

    # Use unique keys for each input widget by appending scenario index
    house_price = st.number_input(
        "Home Price ($)", value=scenario["house_price"], step=10000, format="%i", key=f"house_price_{i}"
    )
    down_payment_pct = st.number_input(
        "Down Payment (%)", min_value=0.0, max_value=100.0, value=scenario["down_payment_pct"], step=0.5, format="%.1f", key=f"down_payment_pct_{i}"
    )
    term_option = st.selectbox(
        "Mortgage Term", options=["15 years", "30 years", "Other"], index=1, key=f"term_option_{i}"
    )

    if term_option == "15 years":
        mortgage_term_years = 15
    elif term_option == "30 years":
        mortgage_term_years = 30
    else:
        mortgage_term_years = st.number_input(
            "Custom mortgage term (years)", min_value=1, max_value=50, value=20, key=f"custom_term_{i}"
        )

    interest_rate = st.number_input(
        "Interest Rate (% Annual)", value=scenario["interest_rate"], step=0.1, format="%.2f", key=f"interest_rate_{i}"
    )

    # Update scenario data in session_state
    st.session_state.scenarios[i]["house_price"] = house_price
    st.session_state.scenarios[i]["down_payment_pct"] = down_payment_pct
    st.session_state.scenarios[i]["mortgage_term_years"] = mortgage_term_years
    st.session_state.scenarios[i]["interest_rate"] = interest_rate

    calculator = MortgageCalculator(house_price, down_payment_pct, mortgage_term_years, interest_rate)
    monthly_payment = calculator.monthly_payment

    st.metric(f"Mortgage Payment / Month (Scenario {i + 1})", f"${monthly_payment:,.2f}")

    comparison_results.append({
        "Scenario": f"Scenario {i + 1}",
        "Home Price": house_price,
        "Down Payment %": down_payment_pct,
        "Term (Years)": mortgage_term_years,
        "Interest Rate %": interest_rate,
        "Monthly Payment": monthly_payment,
        "Total Payment": monthly_payment * mortgage_term_years * 12,
        "Total Interest": monthly_payment * mortgage_term_years * 12 - calculator.loan_amount
    })

# Show comparison table
if len(comparison_results) > 1:
    st.markdown("## Scenario Comparison")
    df = pd.DataFrame(comparison_results)
    st.dataframe(df.style.format({
        "Home Price": "${:,.0f}",
        "Monthly Payment": "${:,.2f}",
        "Total Payment": "${:,.2f}",
        "Total Interest": "${:,.2f}",
        "Down Payment %": "{:.1f}%",
        "Interest Rate %": "{:.2f}%",
    }))

    # Optional: Plot monthly payments comparison bar chart
    st.bar_chart(df.set_index("Scenario")["Monthly Payment"])
