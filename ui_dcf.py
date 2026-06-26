############################################################
# UI_DCF.PY
############################################################

import streamlit as st

from charts import (
    revenue_chart,
    fcff_chart,
    pv_chart,
    sensitivity_heatmap
)


############################################################
# DCF TAB
############################################################

def show_dcf_tab(context):

    dcf = context["dcf"]

    sensitivity = context["sensitivity"]

    forecast_df = dcf["forecast_df"]

    sensitivity_df = sensitivity["sensitivity_df"]
    
    ########################################################
    # EXTRACT
    ########################################################

    forecast_df = dcf["forecast_df"]

    ########################################################
    # SUMMARY
    ########################################################

    st.header("DCF Valuation")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Enterprise Value",
        f"{dcf['enterprise_value']:,.0f} M"
    )

    c2.metric(
        "Equity Value",
        f"{dcf['equity_value']:,.0f} M"
    )

    c3.metric(
        "Terminal Value",
        f"{dcf['terminal_value']:,.0f} M"
    )

    c4.metric(
        "Fair Value",
        f"Rs {dcf['fair_value']:,.2f}"
    )

    ########################################################
    # FORECAST TABLE
    ########################################################

    st.divider()

    st.subheader("DCF Forecast")

    st.dataframe(

        forecast_df.style.format({
    
            "Revenue":"{:,.0f}",
    
            "EBIT":"{:,.0f}",
    
            "NOPAT":"{:,.0f}",
    
            "Depreciation":"{:,.0f}",
    
            "Capex":"{:,.0f}",
    
            "Δ Working Capital":"{:,.0f}",
    
            "FCFF":"{:,.0f}",
    
            "PV FCFF":"{:,.0f}"
    
        }),
    
        use_container_width=True,
    
        hide_index=True
    
    )

    ########################################################
    # CHARTS
    ########################################################

#    st.divider()

#    st.subheader("DCF Charts")

#    st.plotly_chart(

#        revenue_chart(forecast_df),

#        use_container_width=True

#    )

#    st.plotly_chart(

#        fcff_chart(forecast_df),

#        use_container_width=True

#    )

#    st.plotly_chart(

#        pv_chart(forecast_df),

#        use_container_width=True

#    )

    ########################################################
    # SENSITIVITY
    ########################################################

    st.divider()

    st.subheader("Sensitivity Analysis")

    st.dataframe(

        sensitivity_df,

        use_container_width=True

    )

    st.plotly_chart(

        sensitivity_heatmap(

            sensitivity_df

        ),

        use_container_width=True

    )

#######################
