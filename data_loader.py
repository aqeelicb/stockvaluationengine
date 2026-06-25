############################################################
# data_loader.py
# StocksValue
############################################################

import streamlit as st
import pandas as pd


def load_data(uploaded_file):

    """
    Reads the uploaded Excel workbook
    and returns all required data objects.
    """

    ########################################################
    # READ SHEETS
    ########################################################

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

        st.error(
            f"Error reading workbook:\n{e}"
        )

        st.stop()

    ########################################################
    # COMPANY
    ########################################################

    company = {

        "name": company_df.iloc[0,0],

        "ticker": company_df.iloc[0,1]

    }

    ########################################################
    # MARKET DICTIONARY
    ########################################################

    market_dict = dict(

        zip(

            market_df["Variable"],

            market_df["Value"]

        )

    )

    ########################################################
    # INDUSTRY
    ########################################################

    industry = {

        "pe": float(

            industry_df["PE"].iloc[0]

        ),

        "ps": float(

            industry_df["PS"].iloc[0]

        ),

        "ev_ebitda": float(

            industry_df["EV_EBITDA"].iloc[0]

        )

    }

    ########################################################
    # WEIGHTS
    ########################################################

    weights = {

        "dcf":

        float(

            weights_df.loc[

                weights_df["Method"]=="DCF",

                "Weight"

            ].iloc[0]

        ),

        "pe":

        float(

            weights_df.loc[

                weights_df["Method"]=="PE",

                "Weight"

            ].iloc[0]

        ),

        "ps":

        float(

            weights_df.loc[

                weights_df["Method"]=="PS",

                "Weight"

            ].iloc[0]

        ),

        "ev":

        float(

            weights_df.loc[

                weights_df["Method"]=="EV/EBITDA",

                "Weight"

            ].iloc[0]

        )

    }

    ########################################################
    # LATEST FINANCIALS
    ########################################################

    latest = financials.iloc[-1]

    latest_data = {

        "revenue":

        latest["Revenue"],

        "net_income":

        latest["Net_Income"],

        "ebit":

        latest["EBIT"],

        "depreciation":

        latest["Depreciation"],

        "cash":

        latest["Cash"],

        "debt":

        latest["Debt"],

        "shares":

        latest["Shares_Outstanding"]

    }

    ########################################################
    # CURRENT PRICE
    ########################################################

    current_price = float(

        market_dict["Current Market Price"]

    )

    ########################################################
    # CURRENT MULTIPLES
    ########################################################

    market_cap = (

        current_price

        *

        latest_data["shares"]

    )

    eps = (

        latest_data["net_income"]

        /

        latest_data["shares"]

    )

    current_pe = (

        current_price

        /

        eps

        if eps != 0

        else 0

    )

    current_ps = (

        market_cap

        /

        latest_data["revenue"]

        if latest_data["revenue"] != 0

        else 0

    )

    market_ev = (

        market_cap

        +

        latest_data["debt"]

        -

        latest_data["cash"]

    )

    ebitda = (

        latest_data["ebit"]

        +

        latest_data["depreciation"]

    )

    current_ev_ebitda = (

        market_ev

        /

        ebitda

        if ebitda != 0

        else 0

    )

    ########################################################
    # RETURN EVERYTHING
    ########################################################

    return {

        "company": company,

        "financials": financials,

        "market_df": market_df,

        "industry_df": industry_df,

        "weights_df": weights_df,

        "market_dict": market_dict,

        "industry": industry,

        "weights": weights,

        "latest": latest_data,

        "current_price": current_price,

        "market_cap": market_cap,

        "market_ev": market_ev,

        "current_pe": current_pe,

        "current_ps": current_ps,

        "current_ev_ebitda": current_ev_ebitda

    }

