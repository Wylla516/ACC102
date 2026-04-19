# ACC102
# ACC102 Mini Assignment - Track 4: Interactive Financial Analysis Tool
S&P 500 Corporate Financial Ratio Analysis (2020–2024)

## 1. Problem & User
This project solves the difficulty of manually comparing and interpreting large volumes of corporate financial performance data across multiple years. It delivers a simplified, interactive dashboard for ACC102 students, beginner investors, and financial learners to quickly assess S&P 500 company profitability and risk without advanced technical expertise.

## 2. Data
Source: WRDS (Wharton Research Data Services) academic financial database
Access Date: April 10, 2026
Time Period: 2020–2024
Key Fields & Calculated Metrics: Total assets, total equity, total debt, net income, total revenue; derived ratios including ROA, ROE, debt-to-asset ratio, and net profit margin.

## 3. Methods (main Python steps)
Import raw WRDS financial dataset into Pandas DataFrame
Perform data cleaning: remove null values, filter invalid outliers, standardize column names
Code custom formulas to calculate core financial ratios
Conduct exploratory trend analysis and cross-year comparison
Build interactive filtering, dropdown selection and dynamic visualization with Streamlit
Resolve matplotlib rendering compatibility conflicts for cloud deployment
Deploy the fully functional dashboard to Streamlit Community Cloud

## 4. Key Findings
There is large variation in profitability (ROA/ROE) performance across different S&P 500 industry sectors over the 5-year window
Company leverage levels (debt-to-asset ratio) remained relatively stable for most large-cap firms between 2020 and 2024
Short-term profit margin volatility was observed around the early period of the dataset
High ROE performance does not always correspond to strong underlying asset efficiency (ROA)
Interactive visualization makes year-over-year financial trend patterns far easier to identify than static tables

## Files Included
- app.py: Streamlit interactive application
- ACC102_WRDS_Analysis1.ipynb: Full data analysis notebook
- wrds_financial_data.csv: Cleaned financial dataset
- README.md: Project documentation
- demo_video.mp4: 1–3 minute demonstration video
- reflection_report.pdf: 500–800 words reflection report

## How to Run Locally
1. Install required packages:
   pip install pandas streamlit
2. Run the app:
   streamlit run app.py

## Product Link
(https://acc102-n374fynaryjmxeta6rxx46.streamlit.app/)

## Author
Yunlu.Wu24
ACC102 2024-25 Semester 2
