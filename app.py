import streamlit as st
import pandas as pd
import os

st.title("WRDS S&P 500 Financial Ratio Analyzer")
st.caption("ACC102 Track 4 | 2020-2024 Data")

# ===== 补充：整体市场趋势图 =====
st.subheader("Overall Market Trend (2020-2024)")
img_path = "C:\\Users\\Wylla\\overall_trend.png"
if os.path.exists(img_path):
    st.image(img_path)

# 读取数据
df = pd.read_csv("wrds_financial_data.csv")

# 公司选择
companies = sorted(df["conm"].unique())
selected = st.selectbox("Select a Company", companies)
df_company = df[df["conm"] == selected]

# 展示比率表格
st.subheader("Key Financial Ratios")
st.dataframe(df_company[["year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]].round(3))

# 展示ROE趋势
st.subheader("ROE Trend")
st.line_chart(df_company, x="year", y="ROE", width="stretch")
