############################################################
# SENSITIVITY.PY
############################################################

import pandas as pd
import numpy as np


############################################################
# DCF SENSITIVITY ANALYSIS
############################################################

def calculate_sensitivity(

    dcf,

    assumptions,

    latest

):

    ########################################################
    # EXTRACT DCF RESULTS
    ########################################################

    forecast_df = dcf["forecast_df"]

    final_fcff = dcf["final_fcff"]

    ########################################################
    # EXTRACT FINANCIALS
    ########################################################

    cash = latest["cash"]

    debt = latest["debt"]

    shares = latest["shares"]

    ########################################################
    # EXTRACT ASSUMPTIONS
    ########################################################

    forecast_years = assumptions["forecast_years"]

    base_wacc = assumptions["wacc"]

    base_growth = assumptions["terminal_growth"]

    ########################################################
    # PV OF EXPLICIT FORECAST
    ########################################################

    pv_forecast = (

        forecast_df["PV FCFF"]

        .sum()

    )

    ########################################################
    # WACC & GROWTH RANGES
    ########################################################

    wacc_values = np.arange(

        base_wacc - 0.02,

        base_wacc + 0.021,

        0.01

    )

    growth_values = np.arange(

        base_growth - 0.01,

        base_growth + 0.011,

        0.01

    )

    ########################################################
    # BUILD TABLE
    ########################################################

    sensitivity = []

    for wacc in wacc_values:

        row = []

        for growth in growth_values:

            ################################################
            # INVALID COMBINATION
            ################################################

            if growth >= wacc:

                row.append(None)

                continue

            ################################################
            # TERMINAL VALUE
            ################################################

            terminal_value = (

                final_fcff

                *

                (

                    1 + growth

                )

            ) / (

                wacc

                -

                growth

            )

            ################################################
            # PV TERMINAL
            ################################################

            pv_terminal = (

                terminal_value

                /

                (

                    (1 + wacc)

                    ** forecast_years

                )

            )

            ################################################
            # ENTERPRISE VALUE
            ################################################

            enterprise_value = (

                pv_forecast

                +

                pv_terminal

            )

            ################################################
            # EQUITY VALUE
            ################################################

            equity_value = (

                enterprise_value

                -

                debt

                +

                cash

            )

            ################################################
            # FAIR VALUE
            ################################################

            fair_value = (

                equity_value

                /

                shares

            )

            row.append(

                round(

                    fair_value,

                    2

                )

            )

        sensitivity.append(

            row

        )

    ########################################################
    # DATAFRAME
    ########################################################

    sensitivity_df = pd.DataFrame(

        sensitivity,

        index=[

            f"{x*100:.1f}%"

            for x in wacc_values

        ],

        columns=[

            f"{x*100:.1f}%"

            for x in growth_values

        ]

    )

    ########################################################
    # RETURN
    ########################################################

    return {

        "sensitivity_df": sensitivity_df

    }
