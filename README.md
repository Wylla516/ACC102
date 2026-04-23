# 📊 ACC102 Track 4: Advanced S&P 500 Corporate Financial Analysis Dashboard
Student: Yunlu Wu | ACC102 Course Mini Assignment

---

## 🎯 1. Problem & Intended User
This interactive dashboard addresses the challenge of efficiently interpreting complex corporate financial statements for academic and practical accounting analysis.
It transforms raw WRDS financial data into an easy-to-navigate, fully interactive platform that visualises multi-year profitability, leverage and operational risk trends.
The primary intended users are ACC102 course students, junior financial analysts, and academic learners who need to conduct structured performance benchmarking between individual listed firms and the overall S&P 500 market average.

---

## 📂 2. Dataset Information
- **Primary Data Source**: WRDS Compustat Fundamentals Annual Database (official academic industry standard financial dataset)
- **Data Access Date**: **April 10, 2026**
- **Data Access Period**: 5 full fiscal years, 2020 – 2024
- **Data Acquisition Method**: Direct live SQL query via official WRDS Python API connection
- **Core Raw Variables Pulled**:
  - `conm`: Full registered company name
  - `fyear`: Fiscal year of record
  - `at`: Total company assets
  - `lt`: Total company liabilities
  - `ni`: Annual net income
  - `revt`: Total operating revenue
  - `dltt`: Long term corporate debt
- **Engineered Calculated Metrics**:
  - ROA (Return on Assets)
  - ROE (Return on Equity)
  - Debt-to-Asset leverage ratio
  - Net profit operating margin
- **Offline Backup**: Pre-cleaned local CSV fallback dataset for cloud deployment compatibility

---

## 🛠️ 3. Technical Implementation & Python Methods
1. Environment & Compatibility Setup: Built native error-resistant WRDS auto-install logic, supports both local full live connection and cloud offline fallback mode
2. Secure Database Connection: Credential gated WRDS authentication session creation
3. Raw Data Extraction: Structured SQL filtering to extract standardised, consolidated industrial financial records
4. Data Preprocessing & Cleaning:
   - Removal of incomplete null-value records
   - Outlier capping to eliminate extreme abnormal financial noise
   - Data type standardisation and duplicate entry removal
   - Sampling limited to top 200 firms for optimal dashboard runtime speed
5. Financial Calculations: Computation of 4 core industry standard financial performance ratios
6. Interactive Interface Build:
   - Full sidebar year range slider filter
   - Real-time company name keyword search function
   - Dynamic single company selection module
7. Visualisation Generation: Created 9 fully native Streamlit interactive charts for trend, comparison and correlation analysis
8. Advanced Analytical Framework: Built-in automated DuPont decomposition, PEST macro environment evaluation and dynamic financial risk rating system

---

## 📈 4. Key Project Insights & Findings
- Across the 2020–2024 window, most S&P 500 firms show significant profitability volatility directly linked to post-pandemic macroeconomic recovery and interest rate fluctuation cycles
- Higher corporate debt leverage consistently amplifies ROE returns, but also significantly increases long term financial downside risk
- Companies with strong stable operational profit margins maintain far more consistent ROA and ROE performance compared to peers reliant on debt financing
- Most sampled firms maintain debt asset ratios below the 60% moderate risk threshold
- Peak profitability periods for most businesses align with economic recovery years, while trough performance correlates with inflation and market contraction events
- There is a strong consistent positive correlation between ROA and ROE across the majority of analysed corporations

---

## 🚀 5. How To Run This Project
### Option 1: Local Full WRDS Live Mode (Recommended for Full Grading Eligibility)
1. Clone or download the full repository to your local device
2. Install all required project dependencies via command:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the dashboard application:
   ```bash
   streamlit run app.py
   ```
4. Enter your personal WRDS account username and password
5. Click `Connect to WRDS` to load the full live official dataset

### Option 2: Cloud Streamlit Hosted Mode
1. Visit the public deployed Streamlit web link
2. The dashboard will automatically detect cloud environment limitations
3. Offline cleaned backup dataset will load automatically with zero additional configuration
4. All interactive charts, filters and analysis features remain fully functional

---

## 🔗 6. Live Product Demo & Deployment
1. ✅ **Official Deployed Dashboard Link**: [https://acc102-m4zgfcfszz6fjggrfqfa32.streamlit.app/]
2. ✅ **Full Interactive Functionality**: All 9 charts, filters and academic analysis modules fully operational
3. ✅ **Assignment Demo Video**: 1–3 minute walkthrough presentation video submitted alongside this repository
4. ✅ **Local Performance**: Full original WRDS direct database connection functionality preserved for submission grading

---

## ⚠️ 7. Project Limitations & Future Improvements
### Current Project Limitations
- This analysis only utilises annual consolidated fiscal data, and does not include quarterly interim financial records for higher frequency trend observation
- Benchmark comparison is only completed against the overall general market average, with no dedicated industry sector peer grouping
- External macroeconomic indicator variables are referenced qualitatively but not numerically integrated into the dataset
- Does not incorporate advanced predictive or regression modelling for forward performance forecasting

### Planned Future Optimisation Steps
1. Integrate quarterly financial dataset to improve analysis granularity and short term trend visibility
2. Add dedicated industry sector classification and grouped peer benchmark comparison functionality
3. Expand analysis with additional advanced DuPont 3-part full decomposition breakdown
4. Integrate external interest rate, inflation and market index data for deeper economic context
5. Add downloadable custom report export function for analysed company results
