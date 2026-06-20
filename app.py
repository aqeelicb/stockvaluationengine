############################################################
# STOCK VALUATION ENGINE
# VERSION 1 - PART 1
# DATA IMPORT & HISTORICAL ANALYSIS
#
# Author: Muhammad Aqeel
############################################################

############################################################
# IMPORT LIBRARIES
############################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

############################################################
# PAGE CONFIGURATION
############################################################

st.set_page_config(
    page_title="Stock Valuation Engine by Aqeel",
    layout="wide"
)


############################################################
# APP TITLE
############################################################

st.title("📈 Stock Valuation Engine by Aqeel")

st.caption(
    "Financial Data: PKR Million | Forecast Charts: PKR Billion | Fair Value: PKR per Share")

############################################################
# DOWNLOAD EXCEL TEMPLATE
############################################################

try:

    with open(
        "valuation_template.xlsx",
        "rb"
    ) as template_file:

        st.download_button(
            label="📥 Download Valuation Template",
            data=template_file,
            file_name="valuation_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

except:

    st.warning(
        "Valuation template file not found."
    )

st.markdown(
"""
Upload the valuation template Excel file to begin analysis.
"""
)

############################################################
# FILE UPLOAD
############################################################

uploaded_file = st.file_uploader(
    "Upload Excel Workbook",
    type=["xlsx"]
)

############################################################
# STOP IF NO FILE UPLOADED
############################################################

if uploaded_file is None:

    st.info("Please upload the Excel template.")
    st.stop()

############################################################
# READ EXCEL SHEETS
############################################################

try:

    company_df = pd.read_excel(
        uploaded_file,
        sheet_name="Company"
    )

    financials = pd.read_excel(
        uploaded_file,
        sheet_name="Financial_data"
    )

    market_df = pd.read_excel(
        uploaded_file,
        sheet_name="Market_data"
    )

    industry_df = pd.read_excel(
        uploaded_file,
        sheet_name="Industry_data"
    )

    weights_df = pd.read_excel(
        uploaded_file,
        sheet_name="Valuation_weights"
    )

except Exception as e:

    st.error(f"Error reading workbook: {e}")
    st.stop()

############################################################
# COMPANY INFORMATION
############################################################

company_name = company_df.iloc[0, 0]
ticker = company_df.iloc[0, 1]

st.success(
    f"Company: {company_name} | Ticker: {ticker}"
)

############################################################
# SHOW FINANCIAL DATA
############################################################

st.header("Historical Financial Data")

st.dataframe(
    financials,
    use_container_width=True
)

############################################################
# CALCULATE HISTORICAL METRICS
############################################################

############################################################
# REVENUE CAGR
############################################################

first_revenue = financials["Revenue"].iloc[0]
last_revenue = financials["Revenue"].iloc[-1]

num_years = len(financials) - 1

revenue_cagr = (
    (last_revenue / first_revenue)
    ** (1 / num_years)
) - 1

############################################################
# EBIT MARGIN
############################################################

financials["EBIT_Margin"] = (
    financials["EBIT"]
    /
    financials["Revenue"]
)

avg_ebit_margin = (
    financials["EBIT_Margin"]
    .mean()
)

############################################################
# INVESTING CASH FLOW %
############################################################

financials["Investing_Pct"] = (
    financials["Investing_Cash_Flow"]
    /
    financials["Revenue"]
)

avg_investing_pct = (
    financials["Investing_Pct"]
    .mean()
)

############################################################
# WORKING CAPITAL %
############################################################

financials["WC_Pct"] = (
    financials["Working_Capital"]
    /
    financials["Revenue"]
)

avg_wc_pct = (
    financials["WC_Pct"]
    .mean()
)

############################################################
# DEPRECIATION %
############################################################

financials["Dep_Pct"] = (
    financials["Depreciation"]
    /
    financials["Revenue"]
)

avg_dep_pct = (
    financials["Dep_Pct"]
    .mean()
)

############################################################
# DISPLAY HISTORICAL METRICS
############################################################

st.header("Historical Analysis")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Revenue CAGR",
    f"{revenue_cagr:.2%}"
)

col2.metric(
    "Avg EBIT Margin",
    f"{avg_ebit_margin:.2%}"
)

col3.metric(
    "Avg Investing CF %",
    f"{avg_investing_pct:.2%}"
)

col4.metric(
    "Avg Working Capital %",
    f"{avg_wc_pct:.2%}"
)

col5.metric(
    "Avg Depreciation %",
    f"{avg_dep_pct:.2%}"
)

############################################################
# MARKET DATA
############################################################

st.header("Market Assumptions")

market_dict = dict(
    zip(
        market_df["Variable"],
        market_df["Value"]
    )
)

st.dataframe(
    market_df,
    use_container_width=True
)

############################################################
# DEBUG SECTION
############################################################

with st.expander("Debug Information"):

    st.write("Company Sheet")
    st.dataframe(company_df)

    st.write("Market Sheet")
    st.dataframe(market_df)

    st.write("Industry Sheet")
    st.dataframe(industry_df)

    st.write("Weights Sheet")
    st.dataframe(weights_df)

############################################################
# END OF PART 1
############################################################

############################################################
# PART 2 WILL CONTAIN:
#
# 1. CAPM COST OF EQUITY
# 2. WACC
# 3. DCF FORECAST
# 4. TERMINAL VALUE
# 5. ENTERPRISE VALUE
# 6. EQUITY VALUE
# 7. FAIR VALUE PER SHARE
# 8. MANUAL OVERRIDE
# 9. REVENUE CHART
# 10. FCFF CHART
#
############################################################

############################################################

# PART 2

# DCF ENGINE

############################################################

import plotly.graph_objects as go

############################################################

# CONVERT MARKET DATA TO DICTIONARY

############################################################

market_dict = dict(
zip(
market_df["Variable"],
market_df["Value"]
)
)

############################################################

# EXTRACT MARKET ASSUMPTIONS

############################################################

risk_free_rate = float(
market_dict.get("Risk Free Rate", 12)
)

market_erp = float(
market_dict.get("Market ERP", 6)
)

beta = float(
market_dict.get("Beta", 1)
)

cost_of_debt = float(
market_dict.get("Cost of Debt", 12)
)

tax_rate = float(
market_dict.get("Tax Rate", 29)
)

forecast_years = int(
market_dict.get("Forecast Years", 5)
)

terminal_growth = float(
market_dict.get("Terminal Growth", 3)
)

############################################################

# LATEST YEAR DATA

############################################################

latest = financials.iloc[-1]

latest_revenue = latest["Revenue"]
latest_debt = latest["Debt"]
latest_cash = latest["Cash"]
latest_shares = latest["Shares_Outstanding"]

############################################################

# CAPM COST OF EQUITY

############################################################

cost_of_equity = (
risk_free_rate
+
beta * market_erp
)

############################################################
# CAPITAL STRUCTURE
############################################################

st.sidebar.subheader("Capital Structure")

equity_weight_pct = st.sidebar.slider(
    "Equity Weight (%)",
    min_value=0,
    max_value=100,
    value=70,
    step=10
)

debt_weight_pct = 100 - equity_weight_pct

st.sidebar.write(
    f"Debt Weight (%): {debt_weight_pct}"
)

equity_weight = equity_weight_pct / 100
debt_weight = debt_weight_pct / 100

############################################################
# WACC
############################################################

wacc = (
    equity_weight * cost_of_equity
    +
    debt_weight * cost_of_debt * (1 - tax_rate / 100)
)

############################################################

# SIDEBAR

############################################################

st.sidebar.header("DCF Assumptions")

assumption_source = st.sidebar.radio(
"Assumption Source",
[
"Historical Average",
"Manual Override"
]
)


############################################################

# HISTORICAL DEFAULTS

############################################################

hist_growth = revenue_cagr
hist_margin = avg_ebit_margin
hist_investing = avg_investing_pct
hist_wc = avg_wc_pct
hist_dep = avg_dep_pct

############################################################
# MANUAL OVERRIDE
############################################################

if assumption_source == "Manual Override":

    growth_rate = st.sidebar.slider(
        "Revenue Growth %",
        -20.0,
        100.0,
        float(hist_growth * 100)
    ) / 100

    ebit_margin = st.sidebar.slider(
        "EBIT Margin %",
        0.0,
        80.0,
        float(hist_margin * 100)
    ) / 100

    investing_pct = st.sidebar.slider(
        "Investing CF % Revenue",
        -50.0,
        50.0,
        float(hist_investing * 100)
    ) / 100

    wc_pct = st.sidebar.slider(
        "Working Capital % Revenue",
        -50.0,
        50.0,
        float(hist_wc * 100)
    ) / 100

    dep_pct = st.sidebar.slider(
        "Depreciation % Revenue",
        0.0,
        20.0,
        float(hist_dep * 100)
    ) / 100

    user_wacc = st.sidebar.slider(
        "WACC %",
        1.0,
        30.0,
        float(wacc * 100)
    ) / 100

    user_terminal_growth = st.sidebar.slider(
        "Terminal Growth %",
        0.0,
        10.0,
        float(terminal_growth)
    ) / 100

else:

    growth_rate = hist_growth
    ebit_margin = hist_margin
    investing_pct = hist_investing
    wc_pct = hist_wc
    dep_pct = hist_dep

    user_wacc = wacc
    user_terminal_growth = terminal_growth / 100


############################################################
# DCF FORECAST
############################################################

forecast_rows = []

revenue = latest_revenue

for year in range(
    1,
    forecast_years + 1
):

    revenue = revenue * (
        1 + growth_rate
    )

    ebit = (
        revenue
        *
        ebit_margin
    )

    nopat = (
        ebit
        *
        (1 - tax_rate / 100)
    )

    depreciation = (
        revenue
        *
        dep_pct
    )

    investing_cf = (
        revenue
        *
        investing_pct
    )

    working_capital = (
        revenue
        *
        wc_pct
    )

    fcff = (
        nopat
        +
        depreciation
        -
        investing_cf
        -
        working_capital
    )

    pv_fcff = (
        fcff
        /
        (
            (1 + user_wacc)
            ** year
        )
    )

    forecast_rows.append([
        year,
        revenue,
        ebit,
        nopat,
        depreciation,
        investing_cf,
        working_capital,
        fcff,
        pv_fcff
    ])

############################################################

# FORECAST DATAFRAME

############################################################

forecast_df = pd.DataFrame(
forecast_rows,
columns=[
"Year",
"Revenue",
"EBIT",
"NOPAT",
"Depreciation",
"Investing_CF",
"Working_Capital",
"FCFF",
"PV_FCFF"
]
)

############################################################

# TERMINAL VALUE

############################################################

final_fcff = (
forecast_df["FCFF"]
.iloc[-1]
)

terminal_fcff = (
final_fcff
*
(
1
+
user_terminal_growth
)
)

terminal_value = (
terminal_fcff
/
(
user_wacc
-
user_terminal_growth
)
)

pv_terminal = (
terminal_value
/
(
(
1
+
user_wacc
)
**
forecast_years
)
)

############################################################

# ENTERPRISE VALUE

############################################################

enterprise_value = (
forecast_df["PV_FCFF"].sum()
+
pv_terminal
)

############################################################

# EQUITY VALUE

############################################################

equity_value = (
enterprise_value
-
latest_debt
+
latest_cash
)

############################################################

# FAIR VALUE PER SHARE

############################################################

fair_value = (
equity_value
/
latest_shares
)

############################################################
# FAIR VALUE RANGE
############################################################

bear_fair_value = fair_value * 0.95

base_fair_value = fair_value

bull_fair_value = fair_value * 1.05



############################################################

# DCF RESULTS

############################################################

st.header("DCF Valuation")

c1, c2, c3 = st.columns(3)

c1.metric(
"Enterprise Value",
f"{enterprise_value:,.0f}"
)

c2.metric(
"Equity Value",
f"{equity_value:,.0f}"
)

c3.metric(
"Fair Value / Share",
f"{fair_value:,.2f}"
)

############################################################
# FAIR VALUE RANGE
############################################################

bear_fair_value = fair_value * 0.95

base_fair_value = fair_value

bull_fair_value = fair_value * 1.05

st.subheader("Fair Value Range")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Bear Case",
    f"Rs {bear_fair_value:,.2f}"
)

col2.metric(
    "Base Case",
    f"Rs {base_fair_value:,.2f}"
)

col3.metric(
    "Bull Case",
    f"Rs {bull_fair_value:,.2f}"
)

############################################################
# DCF SENSITIVITY TABLE
############################################################

st.subheader("DCF Sensitivity Table")

wacc_range = [
    user_wacc - 0.02,
    user_wacc - 0.01,
    user_wacc,
    user_wacc + 0.01,
    user_wacc + 0.02
]

growth_range = [
    user_terminal_growth - 0.01,
    user_terminal_growth,
    user_terminal_growth + 0.01
]

sensitivity_data = []

for g in growth_range:

    row = []

    for w in wacc_range:

        try:

            tv = (
                final_fcff
                * (1 + g)
                /
                (w - g)
            )

            pv_tv = (
                tv
                /
                ((1 + w) ** forecast_years)
            )

            ev = (
                forecast_df["PV_FCFF"].sum()
                +
                pv_tv
            )

            eq = (
                ev
                - latest_debt
                + latest_cash
            )

            fv = (
                eq
                /
                latest_shares
            )

            row.append(
                round(fv, 2)
            )

        except:

            row.append(None)

    sensitivity_data.append(row)

sensitivity_df = pd.DataFrame(

    sensitivity_data,

    columns=[
        f"{w*100:.1f}%"
        for w in wacc_range
    ],

    index=[
        f"{g*100:.1f}%"
        for g in growth_range
    ]
)

sensitivity_df.index.name = "Terminal Growth"

st.markdown(
    "**Columns = WACC | Rows = Terminal Growth**"
)

st.dataframe(
    sensitivity_df,
    use_container_width=True
)

############################################################
# END OF SENSITIVITY ANALYSIS
############################################################

############################################################

# SHOW FORECAST

############################################################

st.subheader(
"DCF Forecast Table"
)

st.dataframe(
forecast_df,
use_container_width=True
)

st.header("DCF Forecast Visualizations")

############################################################
# REVENUE FORECAST CHART
############################################################

st.subheader("Revenue Forecast")

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Revenue"]/1000,
        mode="lines+markers",
        name="Revenue"
    )
)

fig1.update_layout(
    title="Revenue Forecast (DCF)",
    xaxis_title="Forecast Year",
    yaxis_title="Revenue (Rs. Billions)",
    template="plotly_white"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

############################################################
# FCFF FORECAST CHART
############################################################

st.subheader("FCFF Forecast")

fig2 = go.Figure()

fig2.add_trace(
    go.Bar(
        x=forecast_df["Year"],
        y=forecast_df["FCFF"]/1000,
        name="FCFF"
    )
)

fig2.update_layout(
    title="Free Cash Flow to Firm (FCFF)",
    xaxis_title="Forecast Year",
    yaxis_title="FCFF (Rs. Billion)",
    template="plotly_white"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

############################################################

# DCF ASSUMPTIONS TABLE

############################################################

st.subheader(
"DCF Assumptions Used"
)

assumptions_df = pd.DataFrame({

    "Assumption":[
        "Revenue Growth",
        "EBIT Margin",
        "Investing CF %",
        "Working Capital %",
        "Depreciation %",
        "WACC",
        "Terminal Growth"
    ],

    "Value":[
        f"{growth_rate:.2%}",
        f"{ebit_margin:.2%}",
        f"{investing_pct:.2%}",
        f"{wc_pct:.2%}",
        f"{dep_pct:.2%}",
        f"{user_wacc:.2%}",
        f"{user_terminal_growth:.2%}"
    ]
})

st.dataframe(
assumptions_df,
use_container_width=True
)

############################################################

# END OF PART 2

############################################################

