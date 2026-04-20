import streamlit as st
import pandas as pd
import os

st.title("WRDS S&P 500 Financial Ratio Analyzer")
st.caption("ACC102 Track 4 Interactive Tool | 2020-2024 Data")

st.subheader("Overall Market Trend (2020-2024)")
img_path = "overall_trend.png"
if os.path.exists(img_path):
    st.image(img_path)

df = pd.read_csv("wrds_financial_data.csv")

companies = sorted(df["conm"].unique())
selected = st.selectbox("Select a Company", companies)
df_company = df[df["conm"] == selected]

st.subheader("Key Financial Ratios")
st.dataframe(df_company[["year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]].round(3))

st.subheader("ROE Trend")
st.line_chart(df_company, x="year", y="ROE", use_container_width=True)
