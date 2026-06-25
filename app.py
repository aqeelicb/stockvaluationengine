############################################################
# STOCKSVALUE
############################################################

import streamlit as st

from data_loader import load_data

from dcf import run_dcf

from sensitivity import calculate_sensitivity

from multiples import run_multiple_valuation
from sidebar import get_assumptions

from ui_data import show_data_tab
from ui_dcf import show_dcf_tab
from ui_valuation import show_valuation_tab

from pdf_report import create_pdf_report



############################################################
# PAGE CONFIG
############################################################

st.set_page_config(

    page_title="StocksValue by Aqeel",

    page_icon="📈",

    layout="wide"

)

############################################################
# CUSTOM CSS
############################################################

st.markdown(
    """
    <style>

    /* Tab text */
    button[data-baseweb="tab"] {

        font-size: 22px !important;

        font-weight: 700 !important;

        padding: 14px 28px !important;

        height: 65px !important;

        border-radius: 8px 8px 0px 0px !important;
    }

    /* Active tab */
    button[data-baseweb="tab"][aria-selected="true"] {

        background-color: #EAF4FF !important;

        color: #003366 !important;

        border-bottom: 4px solid #1f77b4 !important;

    }

    /* Space between tabs */
    div[data-baseweb="tab-list"]{

        gap:12px;

    }

    </style>
    """,
    unsafe_allow_html=True
)

############################################################
# TITLE
############################################################

st.title("📈 StocksValue by Aqeel")

st.caption(
    "Professional Equity Valuation Platform"
)

############################################################
# FILE UPLOADER
############################################################

uploaded_file = st.file_uploader(

    "Upload Excel Financial Model",

    type=["xlsx"]

)

############################################################
# STOP IF NO FILE
############################################################

if uploaded_file is None:

    st.info(
        "Please upload an Excel file to begin."
    )

    st.stop()

############################################################
# LOAD DATA
############################################################

data = load_data(uploaded_file)

############################################################
# EXTRACT VARIABLES
############################################################

company = data["company"]

financials = data["financials"]

market_df = data["market_df"]

industry_df = data["industry_df"]

weights_df = data["weights_df"]

market_dict = data["market_dict"]

industry = data["industry"]

weights = data["weights"]

latest = data["latest"]

############################################################
# COMPANY
############################################################

company_name = company["name"]

ticker = company["ticker"]

############################################################
# MARKET
############################################################

current_price = data["current_price"]

market_cap = data["market_cap"]

market_ev = data["market_ev"]

############################################################
# CURRENT MULTIPLES
############################################################

current_pe = data["current_pe"]

current_ps = data["current_ps"]

current_ev_ebitda = data["current_ev_ebitda"]

############################################################
# INDUSTRY
############################################################

industry_pe = industry["pe"]

industry_ps = industry["ps"]

industry_ev_ebitda = industry["ev_ebitda"]

############################################################
# WEIGHTS
############################################################

dcf_weight = weights["dcf"]

pe_weight = weights["pe"]

ps_weight = weights["ps"]

ev_weight = weights["ev"]

############################################################
# LATEST FINANCIALS
############################################################

latest_revenue = latest["revenue"]

latest_net_income = latest["net_income"]

latest_ebit = latest["ebit"]

latest_depreciation = latest["depreciation"]

latest_cash = latest["cash"]

latest_debt = latest["debt"]

latest_shares = latest["shares"]

############################################################
# SIDEBAR ASSUMPTIONS
############################################################

assumptions = get_assumptions(

    financials,

    market_dict,

    industry,

    current_pe,

    current_ps,

    current_ev_ebitda

)

############################################################
# EXTRACT ASSUMPTIONS
############################################################

historical_table = assumptions["historical_table"]

############################################################
# DCF
############################################################

dcf = run_dcf(

    latest,

    assumptions

)

############################################################
# SENSITIVITY ANALYSIS
############################################################

sensitivity = calculate_sensitivity(

    dcf,

    assumptions,

    latest

)

sensitivity_df = sensitivity["sensitivity_df"]

forecast_df = dcf["forecast_df"]

fair_value = dcf["fair_value"]

enterprise_value = dcf["enterprise_value"]

equity_value = dcf["equity_value"]

terminal_value = dcf["terminal_value"]

pv_terminal = dcf["pv_terminal"]

final_fcff = dcf["final_fcff"]

############################################################
# MULTIPLE VALUATION
############################################################

valuation = run_multiple_valuation(

    latest,

    assumptions,

    dcf,

    current_price,

    market_cap,

    market_ev,

    weights

)


############################################################
# COMPANY HEADER
############################################################

st.success(

    f"{company_name} ({ticker})"

)

############################################################
# APPLICATION CONTEXT
############################################################

context = {

    "company": company,

    "latest": latest,

    "financials": financials,

    "historical_table": historical_table,

    "market_dict": market_dict,

    "assumptions": assumptions,

    "weights": weights,

    "dcf": dcf,

    "sensitivity": sensitivity,

    "valuation": valuation,

    "industry": industry,

    "current_price": current_price,

    "market_cap": market_cap,

    "market_ev": market_ev

}

#####################################
############# UI DATA ###############


tab1, tab2, tab3 = st.tabs(

    [

        "📋 Data",

        "📈 DCF",

        "💰 Valuation"

    ]

)

with tab1:

    show_data_tab(context)
    
#################### UI DCF #####################

with tab2:

    show_dcf_tab(context)

################### UI VALUATION ################

with tab3:

    show_valuation_tab(context)
