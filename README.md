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

## 5. How to run
Clone or download all project files to your local device
Install required dependencies:
   pip install pandas streamlit
Open terminal in the project folder
Run the comman:
   streamlit run app.py

## 6. Product link / Demo
Live interactive dashboard deployment:
(https://acc102-m4zgfcfszz6fjggrfqfa32.streamlit.app/)
A 1–3 minute demo video showing full tool functionality is also attached in the submission folder.


## 7. Limitations & next steps
Limitations:
Currently only supports single-company individual year trend viewing
No built-in side-by-side multi-company or industry average benchmark comparison
Advanced statistical forecasting and risk scoring functions are not included
Initial outlier and missing value handling can be further refined
Next Steps for Optimization:
Add industry classification filters and sector average benchmark lines
Implement bulk multi-company selection and comparative charts
Add one-click downloadable analysis report function
Further optimize matplotlib chart rendering stability for better visual consistency
Add plain-text financial interpretation guidance for beginner users

## Author
Yunlu.Wu24
ACC102 2024-25 Semester 2
