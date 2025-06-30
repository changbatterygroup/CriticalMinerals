# App/components/form.py
from dash import html, dcc
import App.constants as c
from App.constants import Form as f
from App.components.base import StaticComponent

class FormComponent(StaticComponent):
    def __init__(self):
        self.layout = html.Div([
            dcc.Dropdown(id=f.CATHODE_DROPDOWN_ID.value, options=c.NMC, value=c.NMC[0], clearable=False),
            html.Br(),
            html.Div([
                html.Label(id=f.NMC_LABEL_ID.value ,style={'font-weight': 'bold', 'padding-right': '12px'}),
                dcc.Slider(id=f.NMC_INPUT_ID.value, min=0, max=100, step = 5, value=50, marks={
                    i: str(i) + '%' for i in range(0, 101, 25)}),
                
            ]),
            
            html.Div([
                html.Label(id=f.P_PCT.value, style={'font-weight': 'bold', 'padding-right': '10px'}),
                dcc.Slider(id=f.P_INPUT_ID.value, min=10, max=30, step=2 ,marks={
                    i: str(i) + '%' for i in range(10, 30+1, 10)}, value=25) 
            ]),
            
        ], id="form-box")
