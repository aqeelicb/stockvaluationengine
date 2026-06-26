############################################################
# SIDEBAR.PY
############################################################

import streamlit as st
import pandas as pd


############################################################
# BUILD SIDEBAR
############################################################

def get_assumptions(

    financials,

    market_dict,

    industry,

    current_pe,

    current_ps,

    current_ev_ebitda

):

    ########################################################
    # HISTORICAL METRICS
    ########################################################

    first_revenue = financials["Revenue"].iloc[0]

    last_revenue = financials["Revenue"].iloc[-1]

    num_years = len(financials) - 1

    revenue_cagr = (

        (last_revenue / first_revenue)

        **

        (1 / num_years)

    ) - 1

    ########################################################
    # EBIT MARGIN
    ########################################################

    financials["EBIT_Margin"] = (

        financials["EBIT"]

        /

        financials["Revenue"]

    )

    avg_ebit_margin = (

        financials["EBIT_Margin"]

        .mean()

    )

    ########################################################
    # Capex %
    ########################################################

    financials["Capex_Pct"] = (

        financials["Capex"]

        /

        financials["Revenue"]

    )

    avg_Capex_pct = (

        financials["Capex_Pct"]

        .mean()

    )

    ########################################################
    # CHANGE IN WC
    ########################################################

    financials["WC_Change"] = (

        financials["Working_Capital"]

        .diff()

    )

    financials["WC_Change_Pct"] = (

        financials["WC_Change"]

        /

        financials["Revenue"]

    )

    avg_wc_change_pct = (

        financials["WC_Change_Pct"]

        .iloc[1:]

        .mean()

    )

    ########################################################
    # DEPRECIATION
    ########################################################

    financials["Dep_Pct"] = (

        financials["Depreciation"]

        /

        financials["Revenue"]

    )

    avg_dep_pct = (

        financials["Dep_Pct"]

        .mean()

    )

    ########################################################
    # MARKET INPUTS
    ########################################################

    risk_free_rate = float(

        market_dict["Risk Free Rate"]

    )

    market_erp = float(

        market_dict["Market ERP"]

    )

    beta = float(

        market_dict["Beta"]

    )

    cost_of_debt = float(

        market_dict["Cost of Debt"]

    )

    tax_rate = float(

        market_dict["Tax Rate (Effective)"]

    )

    forecast_years = int(

        market_dict["Forecast years"]

    )

    terminal_growth = float(

        market_dict["Terminal growth"]

    )

    ########################################################
    # DEFAULT ASSUMPTIONS
    ########################################################

    growth_rate = revenue_cagr

    ebit_margin = avg_ebit_margin

    Capex_pct = avg_Capex_pct

    wc_pct = avg_wc_change_pct

    dep_pct = avg_dep_pct

    ########################################################
    # DEFAULT CAPITAL STRUCTURE
    ########################################################

    equity_weight_pct = 70

    debt_weight_pct = 30

    ########################################################
    # SIDEBAR
    ########################################################

    st.sidebar.header("Valuation Assumptions")

    assumption_source = st.sidebar.radio(

        "Assumption Source",

        [

            "Historical Average",

            "Manual Override"

        ]

    )

    ########################################################
    # DCF ASSUMPTIONS
    ########################################################

    if assumption_source == "Manual Override":

        st.sidebar.subheader("📈 DCF Assumptions")

        growth_rate = st.sidebar.slider(

            "Revenue Growth %",

            -20.0,

            100.0,

            float(growth_rate * 100),

            step=0.5

        ) / 100

        ebit_margin = st.sidebar.slider(

            "EBIT Margin %",

            0.0,

            80.0,

            float(ebit_margin * 100),

            step=0.05

        ) / 100

        Capex_pct = st.sidebar.slider(

            "Capex % Revenue",

            -50.0,

            50.0,

            float(Capex_pct * 100),

            step=0.05

        ) / 100

        wc_pct = st.sidebar.slider(

            "Δ Working Capital % Revenue",

            -20.0,

            20.0,

            float(wc_pct * 100),

            step=0.1

        ) / 100

        dep_pct = st.sidebar.slider(

            "Depreciation % Revenue",

            0.0,

            20.0,

            float(dep_pct * 100),

            step=0.1

        ) / 100

        tax_rate = st.sidebar.slider(

            "Tax Rate %",

            0.0,

            60.0,

            float(tax_rate * 100),

            step=1.0

        ) / 100

    ########################################################
    # DISCOUNT RATE
    ########################################################

    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Discount Rate")

    if assumption_source == "Manual Override":

        risk_free_rate = st.sidebar.slider(
            "Risk Free Rate %",
            0.0,
            25.0,
            float(risk_free_rate * 100),
            step=0.25
        ) / 100

        market_erp = st.sidebar.slider(
            "Market Equity Risk Premium %",
            0.0,
            15.0,
            float(market_erp * 100),
            step=0.25
        ) / 100

        beta = st.sidebar.slider(
            "Beta",
            0.00,
            3.00,
            float(beta),
            step=0.05
        )

        cost_of_debt = st.sidebar.slider(
            "Cost of Debt %",
            0.0,
            30.0,
            float(cost_of_debt * 100),
            step=0.25
        ) / 100

    ########################################################
    # CAPITAL STRUCTURE
    ########################################################

    st.sidebar.markdown("---")
    st.sidebar.subheader("🏦 Capital Structure")

    equity_weight_pct = st.sidebar.slider(
        "Equity Weight %",
        0,
        100,
        equity_weight_pct,
        step=5
    )

    debt_weight_pct = 100 - equity_weight_pct

    st.sidebar.caption(
        f"Debt Weight : {debt_weight_pct}%"
    )

    equity_weight = equity_weight_pct / 100
    debt_weight = debt_weight_pct / 100

    ########################################################
    # CAPM
    ########################################################

    cost_of_equity = (

        risk_free_rate

        +

        beta * market_erp

    )

    ########################################################
    # WACC
    ########################################################

    user_wacc = (

        equity_weight

        * cost_of_equity

        +

        debt_weight

        * cost_of_debt

        * (1 - tax_rate)

    )

    st.sidebar.success(
        f"Cost of Equity : {cost_of_equity:.2%}"
    )

    st.sidebar.success(
        f"WACC : {user_wacc:.2%}"
    )

    ########################################################
    # TERMINAL VALUE
    ########################################################

    st.sidebar.markdown("---")
    st.sidebar.subheader("🌱 Terminal Value")

    forecast_years = st.sidebar.slider(
        "Forecast Years",
        3,
        10,
        forecast_years
    )

    terminal_growth = st.sidebar.slider(
        "Terminal Growth %",
        0.0,
        6.0,
        float(terminal_growth * 100),
        step=0.25
    ) / 100

    ########################################################
    # INDUSTRY MULTIPLES
    ########################################################

    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Industry Multiples")

    multiple_source = st.sidebar.radio(

        "Industry Multiples",

        [

            "Historical",

            "Manual Override"

        ]

    )

    selected_pe = industry["pe"]
    selected_ps = industry["ps"]
    selected_ev = industry["ev_ebitda"]

    if multiple_source == "Manual Override":

        selected_pe = st.sidebar.slider(
            "Industry PE",
            1.0,
            30.0,
            float(selected_pe),
            step=0.25
        )

        selected_ps = st.sidebar.slider(
            "Industry PS",
            0.10,
            10.00,
            float(selected_ps),
            step=0.05
        )

        selected_ev = st.sidebar.slider(
            "Industry EV / EBITDA",
            1.0,
            25.0,
            float(selected_ev),
            step=0.25
        )

    ########################################################
    # COMPANY MULTIPLES
    ########################################################

    st.sidebar.markdown("---")
    st.sidebar.subheader("🏢 Company Multiples")

    company_source = st.sidebar.radio(

        "Company Multiples",

        [

            "Historical",

            "Manual Override"

        ]

    )

    company_pe = current_pe
    company_ps = current_ps
    company_ev = current_ev_ebitda

    if company_source == "Manual Override":

        company_pe = st.sidebar.slider(
            "Company PE",
            1.0,
            30.0,
            float(company_pe),
            step=0.25
        )

        company_ps = st.sidebar.slider(
            "Company PS",
            0.10,
            10.00,
            float(company_ps),
            step=0.05
        )

        company_ev = st.sidebar.slider(
            "Company EV / EBITDA",
            1.0,
            25.0,
            float(company_ev),
            step=0.25
        )

    ########################################################
    # HISTORICAL ASSUMPTION TABLE
    ########################################################
    
    historical_table = financials.copy()
    
    ########################################################
    # REVENUE GROWTH
    ########################################################
    
    historical_table["Revenue Growth"] = (
    
        historical_table["Revenue"]
    
        .pct_change()
    
    )
    
    ########################################################
    # EBIT MARGIN
    ########################################################
    
    historical_table["EBIT Margin"] = (
    
        historical_table["EBIT"]
    
        /
    
        historical_table["Revenue"]
    
    )
    
    ########################################################
    # Capex %
    ########################################################
    
    historical_table["Capex %"] = (
    
        historical_table["Capex"]
    
        /
    
        historical_table["Revenue"]
    
    )
    
    ########################################################
    # ΔWC %
    ########################################################
    
    historical_table["ΔWC %"] = (
    
        historical_table["Working_Capital"]
    
        .diff()
    
        /
    
        historical_table["Revenue"]
    
    )
    
    ########################################################
    # DEPRECIATION %
    ########################################################
    
    historical_table["Depreciation %"] = (
    
        historical_table["Depreciation"]
    
        /
    
        historical_table["Revenue"]
    
    )
    
    ########################################################
    # KEEP REQUIRED COLUMNS
    ########################################################
    
    historical_table = historical_table[[
    
        "Year",
    
        "Revenue Growth",
    
        "EBIT Margin",
    
        "Capex %",
    
        "ΔWC %",
    
        "Depreciation %"
    
    ]]

    ########################################################
    # RETURN
    ########################################################

    return {

        # Historical

        "revenue_cagr": revenue_cagr,
        "avg_ebit_margin": avg_ebit_margin,
        "avg_Capex_pct": avg_Capex_pct,
        "avg_wc_change_pct": avg_wc_change_pct,
        "avg_dep_pct": avg_dep_pct,
        "historical_table": historical_table,

        # DCF

        "growth_rate": growth_rate,
        "ebit_margin": ebit_margin,
        "Capex_pct": Capex_pct,
        "wc_pct": wc_pct,
        "dep_pct": dep_pct,
        "tax_rate": tax_rate,

        # Discount Rate

        "risk_free_rate": risk_free_rate,
        "market_erp": market_erp,
        "beta": beta,
        "cost_of_debt": cost_of_debt,
        "cost_of_equity": cost_of_equity,
        "wacc": user_wacc,

        # Forecast

        "forecast_years": forecast_years,
        "terminal_growth": terminal_growth,

        # Capital Structure

        "equity_weight": equity_weight,
        "debt_weight": debt_weight,

        # Industry Multiples

        "selected_pe": selected_pe,
        "selected_ps": selected_ps,
        "selected_ev": selected_ev,

        # Company Multiples

        "company_pe": company_pe,
        "company_ps": company_ps,
        "company_ev": company_ev

    }
