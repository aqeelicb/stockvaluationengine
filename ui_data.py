############################################################
# UI_DATA.PY
############################################################

import streamlit as st
import pandas as pd


############################################################
# DATA TAB
############################################################

def show_data_tab(context):

    ########################################################
    # EXTRACT CONTEXT
    ########################################################

    company = context["company"]

    latest = context["latest"]

    financials = context["financials"]

    historical_table = context["historical_table"]

    market_dict = context["market_dict"]

    assumptions = context["assumptions"]

    valuation = context["valuation"]

    current_price = context["current_price"]

    market_cap = context["market_cap"]

    market_ev = context["market_ev"]
    
    ########################################################
    # CURRENT MULTIPLES
    ########################################################
    
    current_pe = valuation["current_pe"]
    
    current_ps = valuation["current_ps"]
    
    current_ev_ebitda = valuation["current_ev"]
    
    ########################################################
    # HEADER
    ########################################################

    st.header("Company Information")

    c1, c2 = st.columns(2)

    c1.metric(

        "Company",

        company["name"]

    )

    c2.metric(

        "Ticker",

        company["ticker"]

    )

    ########################################################
    # CURRENT MARKET DATA
    ########################################################

    st.divider()

    st.subheader("Current Market Data")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(

        "Current Price",

        f"Rs {current_price:,.2f}"

    )

    c2.metric(

        "Market Cap",

        f"{market_cap:,.0f} M"

    )

    c3.metric(

        "Enterprise Value",

        f"{market_ev:,.0f} M"

    )

    c4.metric(

        "Shares Outstanding",

        f"{latest['shares']:,.2f} M"

    )

    ########################################################
    # CURRENT MULTIPLES
    ########################################################

    st.divider()

    st.subheader("Current Multiples")

    c1,c2,c3 = st.columns(3)

    c1.metric(

        "PE",

        f"{current_pe:.2f}x"

    )

    c2.metric(

        "PS",

        f"{current_ps:.2f}x"

    )

    c3.metric(

        "EV / EBITDA",

        f"{current_ev_ebitda:.2f}x"

    )

    ########################################################
    # HISTORICAL FINANCIALS
    ########################################################

    st.divider()

    st.subheader("Historical Financials")

    st.dataframe(

        financials,

        use_container_width=True,

        hide_index=True

    )

    ########################################################
    # HISTORICAL METRICS
    ########################################################

    st.divider()

    st.subheader("Historical Summary")

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric(

        "Revenue CAGR",

        f"{assumptions['revenue_cagr']:.2%}"

    )

    c2.metric(

        "Avg EBIT Margin",

        f"{assumptions['avg_ebit_margin']:.2%}"

    )

    c3.metric(

        "Avg Capex",

        f"{assumptions['avg_Capex_pct']:.2%}"

    )

    c4.metric(

        "Avg ΔWC",

        f"{assumptions['avg_wc_change_pct']:.2%}"

    )

    c5.metric(

        "Avg Depreciation",

        f"{assumptions['avg_dep_pct']:.2%}"

    )

    ########################################################
    # HISTORICAL ASSUMPTION TABLE
    ########################################################
    
    st.divider()
    
    st.subheader(
        "Historical Assumption Drivers"
    )
    
    styled_table = (
    
        historical_table
    
        .style
    
        .format({
    
            "Revenue Growth":"{:.2%}",
    
            "EBIT Margin":"{:.2%}",
    
            "Capex %":"{:.2%}",
    
            "ΔWC %":"{:.2%}",
    
            "Depreciation %":"{:.2%}"
    
        })
    
        .background_gradient(
    
            cmap="RdYlGn",
    
            subset=[
    
                "Revenue Growth",
    
                "EBIT Margin"
    
            ]
    
        )
    
        .background_gradient(
    
            cmap="Blues",
    
            subset=[
    
                "Depreciation %"
    
            ]
    
        )
    
    )
    
    st.dataframe(
    
        styled_table,
    
        use_container_width=True
    
    )

    ########################################################
    # MARKET INPUTS
    ########################################################

    st.divider()

    st.subheader("Market Inputs")

    market_display = pd.DataFrame({

        "Variable": market_dict.keys(),

        "Value": market_dict.values()

    })

    st.dataframe(

        market_display,

        use_container_width=True,

        hide_index=True

    )

    ########################################################
    # ASSUMPTIONS USED
    ########################################################

    st.divider()

    st.subheader("Assumptions Used")

    assumption_table = pd.DataFrame({

        "Item":[

            "Growth",

            "EBIT Margin",

            "Capex",

            "ΔWC",

            "Depreciation",

            "Tax",

            "WACC",

            "Terminal Growth"

        ],

        "Value":[

            f"{assumptions['growth_rate']:.2%}",

            f"{assumptions['ebit_margin']:.2%}",

            f"{assumptions['Capex_pct']:.2%}",

            f"{assumptions['wc_pct']:.2%}",

            f"{assumptions['dep_pct']:.2%}",

            f"{assumptions['tax_rate']:.2%}",

            f"{assumptions['wacc']:.2%}",

            f"{assumptions['terminal_growth']:.2%}"

        ]

    })

    st.dataframe(

        assumption_table,

        use_container_width=True,

        hide_index=True

    )
