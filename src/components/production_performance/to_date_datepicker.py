from dash import Dash, html
import dash_mantine_components as dmc
from dash.dependencies import Input, Output

# from ...data.loader import ProductionDataSchema
from ...data.source import DataSource 

from .. import ids, cns

def render(app: Dash, source: DataSource) -> html.Div:
    
    @app.callback(
        Output(ids.TO_DATE_DATEPICKER, "value", allow_duplicate=True),
        [
            Input(ids.ALL_DATES_AFTER_CHECKBOX, "checked")
        ], prevent_inital_call=True
    )
    
    def select_latest_date(checked: bool) -> str:
        if checked == True:
            return source.latest_date
        if checked == False:
            pass
            
    return html.Div(
        className=cns.PPD_TO_DATE_PICKER_WRAPPER,
        children=[
            html.H5("To:"),
            
            dmc.DatePicker(
                id=ids.TO_DATE_DATEPICKER,
                className=cns.PPD_TO_DATE_PICKER_DATEPICKER,
                value=source.latest_date,
                dropdownPosition='flip',
                initialLevel='year',
                style={'marginTop':'5px', "width": 175},
            ),

            dmc.Checkbox(
                id=ids.ALL_DATES_AFTER_CHECKBOX,
                className=cns.PPD_TO_DATE_PICKER_BUTTON,
                label='Select the latest date',
                checked=True,
                value=source.latest_date,
                color='dark',
                style={'marginTop':'5px'}
            ),
            
        ]
    )