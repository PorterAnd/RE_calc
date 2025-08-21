import streamlit as st
import pandas as pd

st.title("💵 Cashflow Tracker")

# Attempt to get the mortgage payment from session_state
mortgage_payment_from_calc = st.session_state.get('monthly_mortgage_payment', None)

if mortgage_payment_from_calc is None:
    st.warning("No mortgage payment found. Please visit the Mortgage Calculator page first.")
    use_calc_payment = False
else:
    use_calc_payment = st.radio(
        "Mortgage Payment Source:",
        ("Use payment from Mortgage Calculator", "Enter my own payment"),
        index=0
    ) == "Use payment from Mortgage Calculator"

if use_calc_payment and mortgage_payment_from_calc is not None:
    mortgage_payment = mortgage_payment_from_calc
    st.write(f"Using mortgage payment: ${mortgage_payment:,.2f}")
else:
    mortgage_payment = st.number_input("Enter your mortgage payment", min_value=0.0, value=1000.0, step=50.0)
    st.write(f"Using custom mortgage payment: ${mortgage_payment:,.2f}")

# Input sections for cash inflow and outflow
st.header("Cash Inflow")
total_rental_income = st.number_input("Total Rental Income ($/month)", value=2000.0, step=50.0)
other_revenue = st.number_input("Other Revenue ($/month)", value=0.0, step=10.0)
vacancy_rate = st.number_input("Vacancy Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

st.header("Cash Outflow")
prop_mgmt_pct = st.number_input("Property Management (% of revenue)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
insurance_yearly = st.number_input("Insurance ($/year)", min_value=0.0, value=1200.0, step=50.0)
property_taxes_yearly = st.number_input("Property Taxes ($/year)", min_value=0.0, value=3000.0, step=50.0)
annual_maint_pct = st.number_input("Annual Maintenance (% of revenue)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
utilities_monthly = st.number_input("Utilities ($/month)", min_value=0.0, value=200.0, step=10.0)
hoa_dues_monthly = st.number_input("HOA Dues ($/month)", min_value=0.0, value=0.0, step=10.0)
advertising_yearly = st.number_input("Advertising ($/year)", min_value=0.0, value=600.0, step=50.0)
misc_yearly = st.number_input("Miscellaneous ($/year)", min_value=0.0, value=500.0, step=50.0)
real_estate_sales_fee = st.number_input("Real Estate Sales Fee ($)", min_value=0.0, value=0.0, step=100.0)

submit = st.button("Calculate Cashflow")

if submit:
    effective_rental_income = total_rental_income * (1 - vacancy_rate / 100)
    property_management_fee = effective_rental_income * (prop_mgmt_pct / 100)
    annual_expenses = insurance_yearly + property_taxes_yearly + advertising_yearly + misc_yearly + real_estate_sales_fee
    monthly_expenses = utilities_monthly + hoa_dues_monthly
    annual_maintenance_cost = effective_rental_income * (annual_maint_pct / 100)

    total_monthly_expenses = (
        property_management_fee +
        (annual_expenses / 12) +
        monthly_expenses +
        (annual_maintenance_cost / 12) +
        mortgage_payment
    )

    monthly_cashflow = effective_rental_income + other_revenue - total_monthly_expenses

    st.subheader("Summary")
    st.metric("Monthly Net Cashflow", f"${monthly_cashflow:,.2f}")

    # Optionally, you can build a dataframe with monthly cashflows for visualization
    df = pd.DataFrame({
        "Month": range(1, 13),
        "Net Cashflow": [monthly_cashflow] * 12,
    })
    df["Cumulative Cashflow"] = df["Net Cashflow"].cumsum()

    st.line_chart(df[["Net Cashflow", "Cumulative Cashflow"]])

    with st.expander("View Monthly Cashflow Details"):
        st.dataframe(df)
else:
    st.info("Fill inputs and click 'Calculate Cashflow'")
