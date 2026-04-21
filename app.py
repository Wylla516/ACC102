# ACC102 Track 4 - Interactive Financial Analysis Dashboard
# Student: Yunlu Wu
# Data Source: WRDS S&P 500 (2020-2024)
# Data Access Date: April 12, 2026

import streamlit as st
import pandas as pd
import numpy as np
import os

# --------------------------
# Page Configuration
# --------------------------
# Set page title, icon, and layout
st.set_page_config(
    page_title="S&P 500 Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# Title & Introduction
# --------------------------
st.title("S&P 500 Corporate Financial Performance Dashboard (2020–2024)")
st.markdown("---")
st.markdown("""
This interactive tool supports financial ratio analysis for S&P 500 companies.
Users can view trends in profitability, leverage, and operational efficiency across five years.
All data are sourced from WRDS and processed using Python Pandas.
""")
st.markdown("---")

# --------------------------
# Load and Clean Dataset
# --------------------------
@st.cache_data
def load_data():
    # Load CSV file
    df = pd.read_csv("wrds_financial_data.csv")
    
    # Select key columns and remove missing values
    keep_cols = ["conm", "year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]
    df = df[keep_cols].dropna()

    # Ensure year is integer
    df["year"] = df["year"].astype(int)

    # Filter extreme outliers to ensure valid visualization
    df = df[(df["ROA"].between(-0.5, 0.5))]
    df = df[(df["ROE"].between(-1.0, 1.0))]
    df = df[(df["Debt_Asset"].between(0, 2.0))]
    df = df[(df["Profit_Margin"].between(-2.0, 2.0))]

    # Sort data by company and year
    df = df.sort_values(by=["conm", "year"]).reset_index(drop=True)
    return df

df = load_data()

# --------------------------
# Sidebar - Company Selection
# --------------------------
st.sidebar.header("Control Panel")
st.sidebar.write("Select a company to view financial performance.")

# Create company list
company_list = sorted(df["conm"].dropna().unique())
selected_company = st.sidebar.selectbox("Choose a Company", company_list)

# Filter data for selected company
df_selected = df[df["conm"] == selected_company]

# Stop if no data available
if df_selected.empty:
    st.error("No valid data for this company. Please select another.")
    st.stop()

st.sidebar.write("Selected:", selected_company)
st.markdown("---")

# --------------------------
# Display Financial Data Table
# --------------------------
st.subheader(f"Financial Data Table: {selected_company}")
st.write("Annual financial ratios calculated from WRDS data.")

st.dataframe(
    df_selected[["year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]].round(3),
    use_container_width=True
)
st.markdown("---")

# --------------------------
# Profitability Trend Chart
# --------------------------
st.subheader("Profitability Trend: ROA & ROE")
st.markdown("""
- ROA: Efficiency of using assets to generate profit
- ROE: Return earned for shareholders
- Divergence shows the impact of financial leverage
""")

profit_data = df_selected.set_index("year")[["ROA", "ROE"]]
st.line_chart(profit_data, color=["#FF6B6B", "#4A90E2"])
st.markdown("---")

# --------------------------
# Leverage & Profit Margin Chart
# --------------------------
st.subheader("Leverage & Profit Margin Trend")
st.markdown("""
- Debt-to-Asset Ratio: Measures financial risk and leverage
- Profit Margin: Reflects operating efficiency
""")

risk_data = df_selected.set_index("year")[["Debt_Asset", "Profit_Margin"]]
st.line_chart(risk_data, color=["#FFB74D", "#26A69A"])
st.markdown("---")

# --------------------------
# Five-Year Average Metrics
# --------------------------
st.subheader("Five-Year Average Key Indicators")
col1, col2, col3, col4 = st.columns(4)

avg_roa = df_selected["ROA"].mean(skipna=True).round(3)
avg_roe = df_selected["ROE"].mean(skipna=True).round(3)
avg_debt = df_selected["Debt_Asset"].mean(skipna=True).round(3)
avg_pm = df_selected["Profit_Margin"].mean(skipna=True).round(3)

with col1:
    st.metric("Avg ROA", avg_roa)
with col2:
    st.metric("Avg ROE", avg_roe)
with col3:
    st.metric("Avg Debt/Asset", avg_debt)
with col4:
    st.metric("Avg Profit Margin", avg_pm)

st.markdown("---")

# --------------------------
# Automated Financial Analysis
# --------------------------
st.subheader("Financial Analysis Summary")

st.write(f"**Company:** {selected_company}")
st.write(f"**Analysis Period:** 2020–2024")
st.write(f"**Average ROA:** {avg_roa} | **Average ROE:** {avg_roe}")
st.write(f"**Average Leverage:** {avg_debt} | **Average Profit Margin:** {avg_pm}")

st.write("**Key Interpretation:**")
if avg_roe > avg_roa:
    st.write("- ROE is higher than ROA, indicating positive effects of financial leverage.")
else:
    st.write("- ROE is similar to ROA, showing limited influence of financial leverage.")

if avg_debt > 0.6:
    st.write("- Relatively high leverage → higher financial risk.")
elif avg_debt < 0.3:
    st.write("- Low leverage → conservative capital structure.")
else:
    st.write("- Moderate leverage → balanced financial structure.")

st.write("Trend charts show performance changes across years.")
st.markdown("---")

# --------------------------
# Limitations & Future Improvements
# --------------------------
st.subheader("Limitations & Future Improvements")
st.markdown("""
- Current version supports single-company analysis only.
- No industry benchmark comparison.
- Future versions will add multi-company comparison and industry filters.
""")

# --------------------------
# Footer
# --------------------------
st.caption("ACC102 Track 4 | Developed by Yunlu Wu | Data from WRDS")
