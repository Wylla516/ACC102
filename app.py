# ACC102 Track 4 - Top Tier Full Analysis Dashboard
# Student: Yunlu Wu
# Data Source: Direct WRDS Connection (2020-2024 S&P 500)
# Integrated: WRDS Authentication + 8 Charts + DuPont/PEST/Risk/Market Comparison
# Upgraded: Year Filter + Company Search + Full Interactive Sidebar + Speed Optimized (200 companies only)

try:
    import plotly.express as px
except ImportError:
    px = None
    
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import wrds

# --------------------------
# Page Basic Configuration
# --------------------------
st.set_page_config(
    page_title="S&P 500 Financial Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state to cache data and avoid repeated WRDS connections
if "df" not in st.session_state:
    st.session_state.df = None
if "market_avg" not in st.session_state:
    st.session_state.market_avg = None

# --------------------------
# WRDS Authentication Section
# --------------------------
st.title("Advanced Corporate Financial Performance Analysis (2020–2024)")
st.markdown("---")

st.subheader("🔑 WRDS Database Authentication")
wrds_username = st.text_input("Enter your WRDS Username")
wrds_password = st.text_input("Enter your WRDS Password", type="password")
authenticate_btn = st.button("Connect to WRDS")

# Load cached data to avoid repeated database connections
df = st.session_state.df
market_avg = st.session_state.market_avg

if authenticate_btn:
    if not wrds_username or not wrds_password:
        st.error("❌ Please enter both WRDS username and password!")
    else:
        try:
            # Use cached data if available to improve speed
            if st.session_state.df is not None:
                st.success("✅ Data already loaded (Cached Mode, No Reconnection)")
            else:
                # Establish WRDS connection and retrieve raw data
                db = wrds.Connection(wrds_username=wrds_username, wrds_password=wrds_password)
                st.success("✅ Successfully connected to WRDS Database!")

                # Query financial data from Compustat
                query = """
                SELECT 
                    conm,
                    fyear as year,
                    at,
                    lt,
                    ni,
                    revt,
                    dltt
                FROM 
                    comp.funda
                WHERE 
                    fyear BETWEEN 2020 AND 2024
                    AND indfmt = 'INDL'
                    AND datafmt = 'STD'
                    AND popsrc = 'D'
                    AND consol = 'C'
                """

                raw_df = db.raw_sql(query)
                db.close()

                # Calculate key financial ratios
                raw_df['ROA'] = raw_df['ni'] / raw_df['at']
                raw_df['ROE'] = raw_df['ni'] / raw_df['lt']
                raw_df['Debt_Asset'] = raw_df['dltt'] / raw_df['at']
                raw_df['Profit_Margin'] = raw_df['ni'] / raw_df['revt']

                # Data cleaning and filtering
                df = raw_df.dropna(subset=["conm", "year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]).copy()
                df["year"] = df["year"].astype(int)

                # Remove extreme outliers
                df = df[
                    (df["ROA"].between(-0.5, 0.5)) &
                    (df["ROE"].between(-1.0, 1.0)) &
                    (df["Debt_Asset"].between(0, 1.5)) &
                    (df["Profit_Margin"].between(-1.0, 1.0))
                ]

                # Keep only 200 companies to ensure smooth performance
                unique_firms = df["conm"].unique()[:200]
                df = df[df["conm"].isin(unique_firms)]

                # Sort data and calculate market average
                df = df.sort_values(by=["conm", "year"]).reset_index(drop=True)
                market_avg = df.groupby("year")[["ROA","ROE","Debt_Asset","Profit_Margin"]].mean().reset_index()

                # Save to cache
                st.session_state.df = df
                st.session_state.market_avg = market_avg

                st.success("✅ Data successfully loaded (Optimized for Speed | 200 Companies)")
                st.markdown("---")

        except Exception as e:
            st.error(f"❌ WRDS Connection Failed: {str(e)}")
            st.info("💡 Tips: Check your username/password, or ensure WRDS access is enabled for your account.")

# --------------------------
# Main Dashboard Interface
# --------------------------
if st.session_state.df is not None and st.session_state.market_avg is not None:
    df = st.session_state.df
    market_avg = st.session_state.market_avg

    st.markdown("""
    This interactive dashboard evaluates S&P 500 company financial performance,
    including profitability trends, leverage risk, operating efficiency,
    DuPont decomposition, peak-trough interpretation and external macro PEST analysis.
    Data is directly retrieved from WRDS Compustat database (2020-2024).
    """)
    st.markdown("---")

    # --------------------------
    # Sidebar Control Panel
    # --------------------------
    st.sidebar.header("🎛️ Control Panel")

    # Year range slider
    st.sidebar.subheader("📅 Year Filter")
    available_years = sorted(df["year"].unique())
    start_year, end_year = st.sidebar.slider(
        "Select Year Range",
        min_value=min(available_years),
        max_value=max(available_years),
        value=(min(available_years), max(available_years)),
        step=1
    )

    # Filter data by selected year range
    filtered_df = df[(df["year"] >= start_year) & (df["year"] <= end_year)].copy()

    # Company selection with search function
    st.sidebar.subheader("🏢 Company Selection")
    search_keyword = st.sidebar.text_input("Search Company Name")
    company_list = sorted(filtered_df["conm"].dropna().unique())

    if search_keyword:
        company_list = [name for name in company_list if search_keyword.lower() in name.lower()]

    if len(company_list) > 0:
        selected_company = st.sidebar.selectbox("Choose a Company", company_list, index=0)
    else:
        selected_company = st.sidebar.selectbox("Choose a Company", company_list)

    company_df = filtered_df[filtered_df["conm"] == selected_company].reset_index(drop=True)

    if company_df.empty:
        st.error("No valid data available for this company in selected years.")
        st.stop()

    st.sidebar.write("Selected Company:", selected_company)
    st.sidebar.write("Analyse Period:", f"{start_year} – {end_year}")
    st.markdown("---")

    # --------------------------
    # Financial Data Table
    # --------------------------
    st.subheader(f"Annual Financial Ratio Table: {selected_company}")
    st.dataframe(
        company_df[["year", "ROA", "ROE", "Debt_Asset", "Profit_Margin"]].round(3),
        use_container_width=True
    )
    st.markdown("---")

    # ==============================================
    # Chart 1: ROA & ROE Trend (Dynamic Analysis)
    # ==============================================
    st.subheader("1. Profitability Trend Chart: ROA & ROE")

    profit_chart = company_df.set_index("year")[["ROA", "ROE"]]
    st.line_chart(profit_chart, color=["#FF5A5A", "#4287F5"])

    max_roe_year = company_df.loc[company_df["ROE"].idxmax(), "year"]
    min_roe_year = company_df.loc[company_df["ROE"].idxmin(), "year"]
    roe_trend = "increasing" if company_df["ROE"].iloc[-1] > company_df["ROE"].iloc[0] else "decreasing"
    leverage_gap = company_df["ROE"].mean() - company_df["ROA"].mean()

    st.markdown(f"""
    Dynamic Trend Analysis:
    - {selected_company} achieved its **highest ROE in {max_roe_year}** and **lowest ROE in {min_roe_year}**.
    - The overall ROE trend shows a **{roe_trend}** pattern over the period.
    - The average gap between ROE and ROA is **{leverage_gap:.3f}**, indicating the **impact of financial leverage**.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 2: Leverage & Profit Margin (Dynamic)
    # ==============================================
    st.subheader("2. Leverage & Operating Margin Trend Chart")

    risk_chart = company_df.set_index("year")[["Debt_Asset", "Profit_Margin"]]
    st.line_chart(risk_chart, color=["#FFA947", "#36CBCB"])

    max_debt_year = company_df.loc[company_df["Debt_Asset"].idxmax(), "year"]
    min_debt_year = company_df.loc[company_df["Debt_Asset"].idxmin(), "year"]
    debt_trend = "rising" if company_df["Debt_Asset"].iloc[-1] > company_df["Debt_Asset"].iloc[0] else "declining"
    margin_trend = "improving" if company_df["Profit_Margin"].iloc[-1] > company_df["Profit_Margin"].iloc[0] else "declining"

    st.markdown(f"""
    Dynamic Trend Analysis:
    - {selected_company}’s debt ratio peaked in **{max_debt_year}** and bottomed in **{min_debt_year}**.
    - The debt level shows a **{debt_trend}** trend over the analysis period.
    - Profit margin has been **{margin_trend}** over time, reflecting operational efficiency changes.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 3: Profit Margin Bar Chart (Dynamic)
    # ==============================================
    st.subheader("3. Annual Profit Margin Bar Chart")
    st.bar_chart(company_df.set_index("year")["Profit_Margin"], color="#2E8B57", use_container_width=True)

    best_pm_year = company_df.loc[company_df["Profit_Margin"].idxmax(), "year"]
    worst_pm_year = company_df.loc[company_df["Profit_Margin"].idxmin(), "year"]

    st.markdown(f"""
    Dynamic Analysis:
    - {selected_company} achieved its **strongest profit margin in {best_pm_year}**.
    - Profitability was weakest in **{worst_pm_year}**, reflecting external or internal pressures.
    - The bar chart clearly shows annual variations in operating performance.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 4: Company vs Market Box Plot (UPDATED)
    # ==============================================
    st.subheader("4. Company vs Market Debt Distribution Box Plot")

    df_market = filtered_df.copy()
    df_market["Group"] = "Market (200 Firms)"
    df_comp = company_df.copy()
    df_comp["Group"] = selected_company
    box_data = pd.concat([df_market, df_comp], ignore_index=True)

    fig_box = px.box(
        box_data,
        x="Group",
        y="Debt_Asset",
        color="Group",
        title=f"{selected_company} vs Market Debt Level Comparison",
        color_discrete_map={
            selected_company: "#FF5A5A",
            "Market (200 Firms)": "#8A2BE2"
        }
    )
    fig_box.update_layout(template="plotly_dark")
    st.plotly_chart(fig_box, use_container_width=True)

    comp_debt = company_df["Debt_Asset"].mean()
    market_debt = filtered_df["Debt_Asset"].mean()
    debt_position = "higher than" if comp_debt > market_debt else "lower than"

    st.markdown(f"""
    Dynamic Comparison:
    - {selected_company}’s average debt ratio is **{comp_debt:.3f}**.
    - Market average debt ratio is **{market_debt:.3f}**.
    - This company’s leverage is **{debt_position}** the overall market level.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 5: ROA & ROE Scatter Plot
    # ==============================================
    st.subheader("5. ROA & ROE Correlation Scatter Plot")
    scatter_data = company_df[["year","ROA","ROE"]]
    st.scatter_chart(scatter_data, x="ROA", y="ROE", color="#DC143C", size=150, use_container_width=True)

    corr = company_df[["ROA", "ROE"]].corr().iloc[0,1]

    st.markdown(f"""
    Dynamic Analysis:
    - Correlation coefficient between ROA and ROE: **{corr:.3f}**.
    - A high positive correlation means profitability drivers are **consistent and stable**.
    - Low correlation indicates high sensitivity to financial leverage.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 6: Profitability Area Chart
    # ==============================================
    st.subheader("6. Comprehensive Financial Trend Area Chart")
    area_data = company_df.set_index("year")[["ROA","Profit_Margin"]]
    st.area_chart(area_data, color=["#4682B4","#32CD32"], use_container_width=True)

    st.markdown(f"""
    Dynamic Trend:
    - This chart shows the **cumulative profitability trend** for {selected_company}.
    - Green area = profit margin; blue area = ROA.
    - Expanding areas indicate **improving operational efficiency**.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 7: Company vs Market Benchmark
    # ==============================================
    st.subheader("7. Company VS S&P 500 Market Average Benchmark Comparison")
    compare_df = pd.merge(company_df, market_avg, on="year", suffixes=("_firm","_market"))
    compare_display = compare_df[["year","ROA_firm","ROA_market","ROE_firm","ROE_market"]].set_index("year")
    st.bar_chart(compare_display, use_container_width=True)

    roe_vs_market = "outperforms" if company_df["ROE"].mean() > market_avg["ROE"].mean() else "underperforms"

    st.markdown(f"""
    Dynamic Benchmark Result:
    - {selected_company} **{roe_vs_market}** the market average in terms of ROE.
    - The chart clearly shows annual performance relative to industry peers.
    """)
    st.markdown("---")

    # ==============================================
    # Chart 8: Risk & Volatility Bar Chart
    # ==============================================
    st.subheader("8. Financial Risk & Volatility Horizontal Bar Chart")
    vol_data = pd.DataFrame({
        "Indicator":["ROA Volatility","ROE Volatility","Debt Ratio Level","Profit Level"],
        "Value":[
            round(company_df["ROA"].std(skipna=True),3),
            round(company_df["ROE"].std(skipna=True),3),
            company_df["Debt_Asset"].mean(skipna=True).round(3),
            company_df["Profit_Margin"].mean(skipna=True).round(3)
        ]
    })
    st.bar_chart(vol_data, x="Indicator", y="Value", horizontal=True, color="#FF647C", use_container_width=True)

    st.markdown("""
    Dynamic Risk Analysis:
    - Higher volatility values indicate **less stable** financial performance.
    - Debt ratio level reflects long-term capital structure risk.
    - Profit level shows overall operational return quality.
    """)
    st.markdown("---")

    # --------------------------
    # Average Financial Indicators
    # --------------------------
    st.subheader("Five-Year Average Financial Indicators")
    c1, c2, c3, c4 = st.columns(4)

    avg_roa = company_df["ROA"].mean(skipna=True).round(3)
    avg_roe = company_df["ROE"].mean(skipna=True).round(3)
    avg_debt = company_df["Debt_Asset"].mean(skipna=True).round(3)
    avg_pm = company_df["Profit_Margin"].mean(skipna=True).round(3)

    with c1:
        st.metric("Avg ROA", avg_roa)
    with c2:
        st.metric("Avg ROE", avg_roe)
    with c3:
        st.metric("Avg Debt Ratio", avg_debt)
    with c4:
        st.metric("Avg Profit Margin", avg_pm)

    st.markdown("---")

    # --------------------------
    # DuPont Analysis (Dynamic)
    # --------------------------
    st.subheader("DuPont Decomposition Analysis")
    st.markdown("""
    DuPont core logic:
    ROE = Profit Margin × Asset Turnover × Financial Leverage
    This framework identifies the real driving source of corporate returns.
    """)

    if avg_roe > avg_roa + 0.015:
        st.write(f"""
        {selected_company}’s higher ROE is mainly driven by **strong financial leverage**.
        Debt financing effectively amplifies shareholder returns.
        """)
    elif avg_roe < avg_roa:
        st.write(f"""
        {selected_company} shows **high leverage risk but weak profitability**.
        Debt costs have reduced overall return to shareholders.
        """)
    else:
        st.write(f"""
        {selected_company}’s performance is driven mainly by **operational efficiency**,
        with little contribution from financial leverage.
        """)

    roe_std = round(company_df["ROE"].std(skipna=True), 4)
    st.write(f"Earnings Stability (ROE Standard Deviation): {roe_std}")

    if roe_std < 0.018:
        st.success(f"{selected_company}: Excellent profit stability — low fluctuation.")
    elif roe_std < 0.035:
        st.info(f"{selected_company}: Moderate profit stability — normal fluctuation.")
    else:
        st.warning(f"{selected_company}: Weak profit stability — high fluctuation.")

    st.markdown("---")

    # --------------------------
    # Peak & Trough Dynamic Explanation
    # --------------------------
    st.subheader("Peak & Trough Period Explanation")
    st.markdown(f"""
    - **Peak Performance ({max_roe_year})**: {selected_company} achieved strong profitability
      supported by operational efficiency and favorable market conditions.

    - **Trough Performance ({min_roe_year})**: {selected_company} faced profitability pressure
      from market competition, cost changes, or macroeconomic challenges.
    """)
    st.markdown("---")

    # --------------------------
    # PEST Analysis (Standard Academic Version)
    # --------------------------
    st.subheader("External Macro Environment — PEST Analysis")
    st.markdown("""
    **1. Political Factor**
    Government fiscal policies, financial regulation and industry compliance rules
    directly influence S&P 500 listed firms. Policy changes on taxation and
    corporate borrowing restrictions affect long-term capital structure decisions.

    **2. Economic Factor**
    During 2020–2024, high inflation, fluctuating interest rates and post-pandemic
    economic recovery strongly affected corporate costs, financing expenses and overall profitability.
    Macroeconomic cycles are the core reason for profit fluctuation across five years.

    **3. Social Factor**
    Changing consumer demand, labour cost levels and public health conditions
    influence sales revenue, operating costs and long-term business strategy.
    Market consumption confidence shapes overall operating performance.

    **4. Technological Factor**
    Digital transformation, automation and industrial technological upgrading
    help enterprises optimise cost control, improve asset efficiency 
    and enhance long-term competitive advantages in the capital market.
    """)
    st.markdown("---")

    # --------------------------
    # Risk Rating (Dynamic)
    # --------------------------
    st.subheader("Comprehensive Financial Risk Rating")
    if avg_debt < 0.3:
        st.success(f"Risk Level: Low — {selected_company} maintains a conservative capital structure.")
    elif avg_debt < 0.6:
        st.info(f"Risk Level: Moderate — {selected_company} has a balanced financial structure.")
    else:
        st.warning(f"Risk Level: High — {selected_company} carries relatively high leverage risk.")

    st.markdown("---")

    # --------------------------
    # Limitations
    # --------------------------
    st.subheader("Critical Limitations & Future Improvement")
    st.markdown("""
    This research retrieves data directly from WRDS Compustat but only uses annual consolidated financial data (lacks quarterly analysis).
    No industry sub-sector benchmark comparison is included. Accounting policy differences and
    one-off financial events may affect data accuracy.
    Future optimisation can add industrial sub-sector comparison, macroeconomic indicators and longer time ranges.
    """)

    st.caption("ACC102 Track 4 | Developed by Yunlu Wu | Data Source: WRDS Compustat (Direct Connection)")

else:
    if not authenticate_btn:
        st.info("ℹ️ Please enter your WRDS credentials and click 'Connect to WRDS' to load data.")
