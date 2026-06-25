############################################################
# CHARTS.PY
############################################################

import plotly.express as px

import plotly.graph_objects as go


############################################################
# REVENUE FORECAST
############################################################

def revenue_chart(forecast_df):

    fig = px.line(

        forecast_df,

        x="Year",

        y="Revenue",

        markers=True,

        title="Revenue Forecast"

    )

    fig.update_layout(

        xaxis_title="Year",

        yaxis_title="Revenue"

    )

    return fig


############################################################
# FCFF
############################################################

def fcff_chart(forecast_df):

    fig = px.bar(

        forecast_df,

        x="Year",

        y="FCFF",

        title="Free Cash Flow to Firm"

    )

    return fig


############################################################
# PV FCFF
############################################################

def pv_chart(forecast_df):

    fig = px.bar(

        forecast_df,

        x="Year",

        y="PV FCFF",

        title="Present Value of FCFF"

    )

    return fig


############################################################
# DCF WATERFALL
############################################################

def valuation_chart(

    dcf,

    valuation

):

    methods = [

        "DCF",

        "PE",

        "PS",

        "EV/EBITDA"

    ]

    values = [

        dcf["fair_value"],

        valuation["pe_fair_value"],

        valuation["ps_fair_value"],

        valuation["ev_fair_value"]

    ]

    fig = px.bar(

        x=methods,

        y=values,

        title="Fair Value Comparison"

    )

    return fig


############################################################
# SENSITIVITY HEATMAP
############################################################

def sensitivity_heatmap(

    sensitivity_df

):

    fig = go.Figure(

        data=

        go.Heatmap(

            z=sensitivity_df.values,

            x=sensitivity_df.columns,

            y=sensitivity_df.index,

            text=sensitivity_df.values,

            texttemplate="%{text}",

            colorscale="RdYlGn"

        )

    )

    fig.update_layout(

        title="DCF Sensitivity"

    )

    return fig
  
  
