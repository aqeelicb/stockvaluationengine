############################################################
# DCF.PY
############################################################

import pandas as pd



############################################################
# RUN DCF
############################################################

def run_dcf(

    latest,

    assumptions

):

    ########################################################
    # EXTRACT LATEST FINANCIALS
    ########################################################

    revenue = latest["revenue"]

    cash = latest["cash"]

    debt = latest["debt"]

    shares = latest["shares"]

    ########################################################
    # EXTRACT ASSUMPTIONS
    ########################################################

    growth_rate = assumptions["growth_rate"]

    ebit_margin = assumptions["ebit_margin"]

    investing_pct = assumptions["investing_pct"]

    dep_pct = assumptions["dep_pct"]

    wc_pct = assumptions["wc_pct"]

    tax_rate = assumptions["tax_rate"]

    wacc = assumptions["wacc"]

    terminal_growth = assumptions["terminal_growth"]

    forecast_years = assumptions["forecast_years"]

    ########################################################
    # FORECAST
    ########################################################

    forecast_rows = []

    previous_wc = (

        revenue

        *

        wc_pct

    )

    ########################################################
    # LOOP
    ########################################################

    for year in range(

        1,

        forecast_years + 1

    ):

        revenue = (

            revenue

            *

            (

                1 + growth_rate

            )

        )

        ####################################################
        # OPERATING
        ####################################################

        ebit = (

            revenue

            *

            ebit_margin

        )

        nopat = (

            ebit

            *

            (

                1 - tax_rate

            )

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

        ####################################################
        # WORKING CAPITAL
        ####################################################

        current_wc = (

            revenue

            *

            wc_pct

        )

        wc_change = (

            current_wc

            -

            previous_wc

        )

        previous_wc = current_wc

        ####################################################
        # FCFF
        ####################################################

        fcff = (

            nopat

            +

            depreciation

            -

            investing_cf

            -

            wc_change

        )

        ####################################################
        # PRESENT VALUE
        ####################################################

        pv_fcff = (

            fcff

            /

            (

                (1 + wacc)

                ** year

            )

        )

        ####################################################
        # STORE
        ####################################################

        forecast_rows.append(

            [

                year,

                revenue,

                ebit,

                nopat,

                depreciation,

                investing_cf,

                wc_change,

                fcff,

                pv_fcff

            ]

        )

    ########################################################
    # FORECAST DF
    ########################################################

    forecast_df = pd.DataFrame(

        forecast_rows,

        columns=[

            "Year",

            "Revenue",

            "EBIT",

            "NOPAT",

            "Depreciation",

            "Investing CF",

            "Δ Working Capital",

            "FCFF",

            "PV FCFF"

        ]

    )
    
    ########################################################
    # PV OF FORECAST PERIOD
    ########################################################
    
    pv_forecast = (
    
        forecast_df["PV FCFF"]
    
        .sum()
    
    )

    ########################################################
    # TERMINAL VALUE
    ########################################################

    final_fcff = (

        forecast_df

        .iloc[-1]["FCFF"]

    )

    terminal_value = (

        final_fcff

        *

        (

            1 + terminal_growth

        )

    ) / (

        wacc

        -

        terminal_growth

    )

    ########################################################
    # PV TERMINAL
    ########################################################

    pv_terminal = (

        terminal_value

        /

        (

            (1 + wacc)

            ** forecast_years

        )

    )

    ########################################################
    # ENTERPRISE VALUE
    ########################################################

    enterprise_value = (

        pv_forecast
    
        +
    
        pv_terminal
    
    )

    ########################################################
    # EQUITY VALUE
    ########################################################

    equity_value = (

        enterprise_value

        -

        debt

        +

        cash

    )

    ########################################################
    # FAIR VALUE
    ########################################################

    fair_value = (

        equity_value

        /

        shares

    )

    
    ########################################################
    # RETURN
    ########################################################

    return {

        "forecast_df": forecast_df,
    
        "terminal_value": terminal_value,
    
        "pv_terminal": pv_terminal,
    
        "enterprise_value": enterprise_value,
    
        "equity_value": equity_value,
    
        "fair_value": fair_value,
    
        "final_fcff": final_fcff
    
    }
