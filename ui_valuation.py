############################################################
# UI_VALUATION.PY
############################################################

import streamlit as st

from charts import valuation_chart

from pdf_report import create_pdf_report

############################################################
# VALUATION TAB
############################################################

def show_valuation_tab(context):

    valuation = context["valuation"]

    dcf = context["dcf"]

    weights = context["weights"]

    current_price = context["current_price"]
    
    ########################################################
    # PDF REPORT
    ########################################################
    
    st.divider()
    
    st.subheader("Analyst Report")
    
    pdf = create_pdf_report(context)
    
    st.download_button(
    
        label="📄 Download Analyst Report",
    
        data=pdf,
    
        file_name=f"{context['company']['ticker']}_Analyst_Report.pdf",
    
        mime="application/pdf"
    
    )
    
    ########################################################
    # HEADER
    ########################################################

    st.header("Multiple Valuation")

    ########################################################
    # SUMMARY METRICS
    ########################################################

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(

        "Current Price",

        f"Rs {current_price:,.2f}"

    )

    c2.metric(

        "Weighted Fair Value",

        f"Rs {valuation['weighted_fair_value']:,.2f}"

    )

    c3.metric(

        "Upside",

        f"{valuation['upside']:.2%}"

    )

    c4.metric(

        "Recommendation",

        valuation["signal"]

    )

    ########################################################
    # VALUATION SUMMARY
    ########################################################

    st.divider()

    st.subheader("Valuation Summary")

    st.dataframe(

        valuation["valuation_summary"],

        use_container_width=True,

        hide_index=True

    )

    ########################################################
    # COMPARISON CHART
    ########################################################

    st.divider()

    st.subheader("Fair Value Comparison")

    st.plotly_chart(

        valuation_chart(

            dcf,

            valuation

        ),

        use_container_width=True

    )

    ########################################################
    # WEIGHTS
    ########################################################

    st.divider()

    st.subheader("Weight Allocation")

    weight_table = {

        "Method":[

            "DCF",

            "PE",

            "PS",

            "EV / EBITDA"

        ],

        "Weight":[

            f"{weights['dcf']:.0%}",

            f"{weights['pe']:.0%}",

            f"{weights['ps']:.0%}",

            f"{weights['ev']:.0%}"

        ]

    }

    st.dataframe(

        weight_table,

        hide_index=True,

        use_container_width=True

    )

    ########################################################
    # RECOMMENDATION
    ########################################################

    st.divider()

    st.subheader("Recommendation")

    if valuation["signal"] == "BUY":

        st.success(

            f"The weighted intrinsic value is "

            f"Rs {valuation['weighted_fair_value']:,.2f}, "

            f"which implies an upside of "

            f"{valuation['upside']:.1%}."

        )

    elif valuation["signal"] == "HOLD":

        st.warning(

            f"The stock appears fairly valued "

            f"based on current assumptions."

        )

    else:

        st.error(

            f"The stock appears overvalued "

            f"based on current assumptions."

        )

    ########################################################
    # INVESTMENT LOGIC
    ########################################################

    st.divider()

    st.subheader("Recommendation Logic")

    st.markdown("""

**BUY**

- Upside ≥ 20%

---

**HOLD**

- Upside between 5% and 20%

---

**SELL**

- Upside < 5%

""")
