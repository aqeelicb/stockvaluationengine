############################################################
# PDF_REPORT.PY
############################################################

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors

from reportlab.platypus import PageBreak

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.units import inch

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    TableStyle,

    Image

)

############################################################
# STYLES
############################################################

styles = getSampleStyleSheet()

title_style = styles["Title"]

title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]

############################################################
# HELPER FUNCTIONS
############################################################

def add_heading(elements, text):

    elements.append(

        Paragraph(

            text,

            heading_style

        )

    )

    elements.append(

        Spacer(1, 0.15 * inch)

    )


def add_paragraph(elements, text):

    elements.append(

        Paragraph(

            text,

            normal_style

        )

    )


def add_table(elements, data):

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#003366")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

        ])

    )

    elements.append(table)

    elements.append(

        Spacer(1,0.20*inch)

    )

############################################################
# CREATE REPORT
############################################################

def create_pdf_report(

    context

):

    ########################################################
    # EXTRACT
    ########################################################

    company = context["company"]

    valuation = context["valuation"]

    assumptions = context["assumptions"]

    dcf = context["dcf"]

    industry = context["industry"]

    current_price = context["current_price"]

    ########################################################
    # BUFFER
    ########################################################

    buffer = BytesIO()

    doc = SimpleDocTemplate(

        buffer,

        rightMargin=25,

        leftMargin=25,

        topMargin=25,

        bottomMargin=25

    )

    elements = []

    ########################################################
    # TITLE
    ########################################################

    elements.append(

        Paragraph(

            "StocksValue by Aqeel",

            title_style

        )

    )

    elements.append(

        Paragraph(

            "Equity Valuation Report",

            heading_style

        )

    )

    elements.append(

        Spacer(1,0.25*inch)

    )

    ########################################################
    # COMPANY INFORMATION
    ########################################################

    report_time = datetime.now().strftime(

        "%d-%b-%Y %I:%M %p"

    )

    company_table = [

        ["Company", company["name"]],

        ["Ticker", company["ticker"]],

        ["Generated", report_time]

    ]

    add_table(

        elements,

        company_table

    )

    ########################################################
    # EXECUTIVE SUMMARY
    ########################################################

    add_heading(

        elements,

        "Executive Summary"

    )

    summary_table = [

        ["Metric","Value"],

        [

            "Current Price",

            f"Rs {current_price:,.2f}"

        ],

        [

            "DCF Fair Value",

            f"Rs {dcf['fair_value']:,.2f}"

        ],

        [

            "Weighted Fair Value",

            f"Rs {valuation['weighted_fair_value']:,.2f}"

        ],

        [

            "Upside",

            f"{valuation['upside']:.1%}"

        ],

        [

            "Recommendation",

            valuation["signal"]

        ]

    ]

    add_table(

        elements,

        summary_table

    )

    ########################################################
    # VALUATION SUMMARY
    ########################################################

    add_heading(

        elements,

        "Valuation Summary"

    )

    valuation_table = [

        [

            "Method",

            "Company",

            "Benchmark",

            "Fair Value"

        ]

    ]

    for _, row in valuation["valuation_summary"].iterrows():

        valuation_table.append(

            [

                row["Method"],

                row["Company Multiple"],

                row["Benchmark"],

                f"Rs {row['Fair Value (Rs)']:,.2f}"

            ]

        )

    add_table(

        elements,

        valuation_table

    )

    ########################################################
    # DCF ASSUMPTIONS
    ########################################################

    add_heading(

        elements,

        "Key DCF Assumptions"

    )

    assumptions_table = [

        ["Assumption","Value"],

        [

            "Revenue Growth",

            f"{assumptions['growth_rate']:.2%}"

        ],

        [

            "EBIT Margin",

            f"{assumptions['ebit_margin']:.2%}"

        ],

        [

            "Tax Rate",

            f"{assumptions['tax_rate']:.2%}"

        ],

        [

            "Investing CF",

            f"{assumptions['investing_pct']:.2%}"

        ],

        [

            "Δ Working Capital",

            f"{assumptions['wc_pct']:.2%}"

        ],

        [

            "Depreciation",

            f"{assumptions['dep_pct']:.2%}"

        ],

        [

            "WACC",

            f"{assumptions['wacc']:.2%}"

        ],

        [

            "Terminal Growth",

            f"{assumptions['terminal_growth']:.2%}"

        ]

    ]

    add_table(

        elements,

        assumptions_table
    )

    ########################################################
    # MULTIPLE ASSUMPTIONS
    ########################################################
    
    elements.append(PageBreak())
    add_heading(
    
        elements,
    
        "Multiple Assumptions"
    
    )
    
    multiple_table = [
    
        [
    
            "Method",
    
            "Company",
    
            "Industry"
    
        ],
    
        [
    
            "PE",
    
            f"{assumptions['company_pe']:.2f}x",
    
            f"{assumptions['selected_pe']:.2f}x"
    
        ],
    
        [
    
            "PS",
    
            f"{assumptions['company_ps']:.2f}x",
    
            f"{assumptions['selected_ps']:.2f}x"
    
        ],
    
        [
    
            "EV / EBITDA",
    
            f"{assumptions['company_ev']:.2f}x",
    
            f"{assumptions['selected_ev']:.2f}x"
    
        ]
    
    ]
    
    add_table(
    
        elements,
    
        multiple_table
    
    )
    
    ########################################################
    # FAIR VALUE SUMMARY
    ########################################################
    
    add_heading(
    
        elements,
    
        "Fair Value Comparison"
    
    )
    
    fair_value_table = [
    
        [
    
            "DCF",
    
            "PE",
    
            "PS",
    
            "EV/EBITDA",
    
            "Weighted"
    
        ],
    
        [
    
            f"Rs {dcf['fair_value']:,.2f}",
    
            f"Rs {valuation['pe_fair_value']:,.2f}",
    
            f"Rs {valuation['ps_fair_value']:,.2f}",
    
            f"Rs {valuation['ev_fair_value']:,.2f}",
    
            f"Rs {valuation['weighted_fair_value']:,.2f}"
    
        ]
    
    ]
    
    add_table(
    
        elements,
    
        fair_value_table
    
    )
    
    ########################################################
    # RECOMMENDATION
    ########################################################
    
    add_heading(
    
        elements,
    
        "Investment View"
    
    )
    
    signal = valuation["signal"]
    
    upside = valuation["upside"] * 100
    
    if signal == "BUY":
    
        colour = "#008000"
    
    elif signal == "HOLD":
    
        colour = "#FF8C00"
    
    else:
    
        colour = "#C00000"
    
    recommendation = f"""
    
    <font color="{colour}">
    
    <b>{signal}</b>
    
    </font>
    
    <br/><br/>
    
    Estimated Upside / Downside:
    
    <b>{upside:.1f}%</b>
    
    """
    
    elements.append(
    
        Paragraph(
    
            recommendation,
    
            normal_style
    
        )
    
    )
    
    elements.append(
    
        Spacer(1,0.20*inch)
    
    )
    
    ########################################################
    # DISCLAIMER
    ########################################################
    
    add_heading(
    
        elements,
    
        "Disclaimer"
    
    )
    
    elements.append(
    
        Paragraph(
    
            "This report has been automatically generated by StocksValue "
            "using financial information supplied by the user. "
            "It is intended solely for educational and informational purposes "
            "and should not be considered investment advice.",
    
            normal_style
    
        )
    
    )
    
    ########################################################
    # BUILD PDF
    ########################################################
    
    doc.build(
    
        elements
    
    )
    
    pdf = buffer.getvalue()
    
    buffer.close()
    
    return pdf
