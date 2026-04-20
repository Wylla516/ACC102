# Import required core Python libraries for web app and data processing
import streamlit as st
import pandas as pd
import os

# App Title & Course Identification
# Set official project name and course assignment label
st.title("WRDS S&P 500 Financial Ratio Analyzer")
st.caption("ACC102 Track 4 Interactive Tool | 2020-2024 Data")

# Section 1: Overall Market Overview
# Display pre-generated full market trend summary chart (if available)
st.subheader("Overall Market Trend (2020-2024)")
img_path = "overall_trend.png"
if os.path.exists(img_path):
    st.image(img_path)
    
# Section 2: Load cleaned financial dataset
# Use relative file path for universal GitHub/Streamlit cloud compatibility
df = pd.read_csv("wrds_financial_data.csv")

# Section 3: Interactive User Selection
# Create dropdown menu for users to pick individual listed company
# Filter dataset to only show selected company records
companies = sorted(df["conm"].unique())
selected = st.selectbox("Select a Company", companies)
df_company = df[df["conm"] == selected]

# Section 4: Display Core Financial Results Table
# Show calculated professional accounting ratios:
# ROA, ROE, Debt-to-Asset Ratio, Profit Margin
# Round values for clean and readable presentation
st.subheader("Key Financial Ratios")
st.dataframe(df_company[["year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]].round(3))

# Section 5: Interactive Trend Visualization
# Plot year-over-year ROE performance for selected company
# Replaced deprecated `use_container_width` parameter
# Avoids Streamlit version warning & matplotlib compatibility conflict
st.subheader("ROE Trend")
st.line_chart(df_company, x="year", y="ROE", width="stretch")
