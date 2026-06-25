############################################################
# MULTIPLES.PY
############################################################

import pandas as pd
from recommendation import get_recommendation

############################################################
# MULTIPLE VALUATION
############################################################

def run_multiple_valuation(

    latest,

    assumptions,

    dcf,

    current_price,

    market_cap,

    market_ev,

    weights

):

    ########################################################
    # LATEST FINANCIALS
    ########################################################

    revenue = latest["revenue"]

    net_income = latest["net_income"]

    ebit = latest["ebit"]

    depreciation = latest["depreciation"]

    debt = latest["debt"]

    cash = latest["cash"]

    shares = latest["shares"]

    ########################################################
    # EBITDA
    ########################################################

    ebitda = (

        ebit

        +

        depreciation

    )

    ########################################################
    # CURRENT MULTIPLES
    ########################################################

    eps = (

        net_income

        /

        shares

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

        revenue

        if revenue != 0

        else 0

    )

    current_ev = (

        market_ev

        /

        ebitda

        if ebitda != 0

        else 0

    )

    ########################################################
    # ASSUMPTIONS
    ########################################################

    company_pe = assumptions["company_pe"]

    company_ps = assumptions["company_ps"]

    company_ev = assumptions["company_ev"]

    industry_pe = assumptions["selected_pe"]

    industry_ps = assumptions["selected_ps"]

    industry_ev = assumptions["selected_ev"]

    ########################################################
    # PE VALUATION
    ########################################################

    pe_fair_value = (

        current_price

        *

        industry_pe

        /

        company_pe

    )

    ########################################################
    # PS VALUATION
    ########################################################

    ps_fair_value = (

        current_price

        *

        industry_ps

        /

        company_ps

    )

    ########################################################
    # EV / EBITDA VALUATION
    ########################################################

    implied_ev = (

        market_ev

        *

        industry_ev

        /

        company_ev

    )

    implied_equity = (

        implied_ev

        -

        debt

        +

        cash

    )

    ev_fair_value = (

        implied_equity

        /

        shares

    )

    ########################################################
    # DCF
    ########################################################

    dcf_fair_value = dcf["fair_value"]

    ########################################################
    # WEIGHTS
    ########################################################

    dcf_weight = weights["dcf"]

    pe_weight = weights["pe"]

    ps_weight = weights["ps"]

    ev_weight = weights["ev"]

    ########################################################
    # WEIGHTED FAIR VALUE
    ########################################################

    weighted_fair_value = (

        dcf_fair_value * dcf_weight

        +

        pe_fair_value * pe_weight

        +

        ps_fair_value * ps_weight

        +

        ev_fair_value * ev_weight

    )

    ########################################################
    # RECOMMENDATION
    ########################################################
    
    recommendation = get_recommendation(
    
        current_price,
    
        weighted_fair_value
    
    )
    
    upside = recommendation["upside"]
    
    signal = recommendation["signal"]
    
    color = recommendation["color"]

    
    ########################################################
    # VALUATION SUMMARY
    ########################################################
    
    valuation_summary = pd.DataFrame({
    
        "Method": [
    
            "DCF",
    
            "PE",
    
            "PS",
    
            "EV/EBITDA"
    
        ],
    
        "Company Multiple": [
    
            "-",
    
            f"{company_pe:.2f}x",
    
            f"{company_ps:.2f}x",
    
            f"{company_ev:.2f}x"
    
        ],
    
        "Benchmark": [
    
            f"WACC {assumptions['wacc']*100:.1f}% | g {assumptions['terminal_growth']*100:.1f}%",
    
            f"{industry_pe:.2f}x",
    
            f"{industry_ps:.2f}x",
    
            f"{industry_ev:.2f}x"
    
        ],
    
        "Fair Value (Rs)": [
    
            round(dcf_fair_value, 2),
    
            round(pe_fair_value, 2),
    
            round(ps_fair_value, 2),
    
            round(ev_fair_value, 2)
    
        ]
    
    })

    ########################################################
    # RETURN
    ########################################################

    return {

        "current_pe": current_pe,

        "current_ps": current_ps,

        "current_ev": current_ev,

        "pe_fair_value": pe_fair_value,

        "ps_fair_value": ps_fair_value,

        "ev_fair_value": ev_fair_value,

        "weighted_fair_value": weighted_fair_value,

        "upside": upside,

        "signal": signal,

        "color": color,
        
        "valuation_summary": valuation_summary
        
    }
