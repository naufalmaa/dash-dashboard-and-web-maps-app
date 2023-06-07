from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import plotly.express as px

from ...data.loader import ProductionDataSchema
from ...data.source import DataSource
from .. import ids, cns

def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.WATER_CUT_GOR_SUBPLOTS, "children", allow_duplicate=True),
        [
            Input(ids.FROM_DATE_DATEPICKER,  "value"),
            Input(ids.TO_DATE_DATEPICKER,    "value"),
            Input(ids.WELL_MAIN_MULTISELECT, "value"),
        ],  prevent_inital_call=True
    )
    
    def update_subplots(from_date: str, to_date: str, wells: list[str]) -> html.Div:
        
        filtered_pt_cum_wc_date = source.filter(from_date=from_date, to_date=to_date, wells=wells).create_pivot_table_date_avg(ProductionDataSchema.WATER_CUT_DAILY)
        filtered_pt_cum_gor_date = source.filter(from_date=from_date, to_date=to_date, wells=wells).create_pivot_table_date_avg(ProductionDataSchema.GAS_OIL_RATIO)
        
        # Create subplots with two y-axes
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add water cut trace to the chart
        fig.add_trace(
            go.Scatter(
                x=filtered_pt_cum_wc_date[ProductionDataSchema.DATE], 
                y=filtered_pt_cum_wc_date[ProductionDataSchema.WATER_CUT_DAILY],
                name='Water Cut', 
                line=dict(color='blue')
                ),
                secondary_y=False
        )

        # Add GOR trace to the chart
        fig.add_trace(
            go.Scatter(
                x=filtered_pt_cum_gor_date[ProductionDataSchema.DATE], 
                y=filtered_pt_cum_gor_date[ProductionDataSchema.GAS_OIL_RATIO],
                name='GOR', 
                line=dict(color='red')
                ),
                secondary_y=True
        )

        # Set y-axis titles
        fig.update_yaxes(title_text="Water Cut (%)", secondary_y=False, range=[-0.5, 10])
        fig.update_yaxes(title_text="GOR (m3/m3)", secondary_y=True, range=[-0.5, 300])

        # Set chart title
        fig.update_layout(
            # title='Daily Water Cut and GOR',
            xaxis_title='Date'
        )
        
        return html.Div(dcc.Graph(figure=fig), id=ids.WATER_CUT_GOR_SUBPLOTS, className=cns.PPD_THIRD_CHART_RIGHT_GRID)

    return html.Div(id=ids.WATER_CUT_GOR_SUBPLOTS, className=cns.PPD_THIRD_CHART_RIGHT_GRID)