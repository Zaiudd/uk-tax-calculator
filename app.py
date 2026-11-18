"""Web page for the UK take-home pay calculator."""

import streamlit as st

from calculator import take_home

PLAN_LABELS = {"none": "No student loan", "plan_2": "Plan 2", "plan_5": "Plan 5"}

st.set_page_config(page_title="UK Take-Home Pay Calculator", page_icon="💷")
st.title("UK Take-Home Pay Calculator")
st.caption("England, Wales and Northern Ireland · 2026/27 tax year · estimates only")

salary = st.number_input(
    "Annual salary (£)", min_value=0, max_value=1_000_000, value=30_000, step=1_000
)
pension = st.slider("Pension contribution (salary sacrifice, %)", 0, 20, 0)
plan = st.selectbox("Student loan", options=list(PLAN_LABELS), format_func=PLAN_LABELS.get)

result = take_home(salary, pension_percent=pension, plan=plan)

col1, col2 = st.columns(2)
col1.metric("Take-home per year", f"£{result['take_home']:,.2f}")
col2.metric("Take-home per month", f"£{result['take_home'] / 12:,.2f}")

st.subheader("Breakdown")
st.dataframe(
    {
        "Item": ["Salary", "Pension", "Income tax", "National Insurance", "Student loan", "Take-home pay"],
        "Per year": [
            f"£{result[key]:,.2f}"
            for key in ["salary", "pension", "income_tax", "national_insurance", "student_loan", "take_home"]
        ],
    },
    hide_index=True,
    use_container_width=True,
)
