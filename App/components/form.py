# App/components/form.py
from dash import html, dcc
import App.constants as c
from App.components.base import StaticComponent

class FormComponent(StaticComponent):
    def __init__(self):
        self.layout = html.Div([
            html.Div([
                html.Label("Porosity %: ", style={'font-weight': 'bold', 'padding-right': '10px'}),
                dcc.Input(id=c.P_INPUT_ID, type='number', placeholder='Enter Porosity', min=0, max=100)
            ]),
            html.Div([
                html.Label("NMC %: ", style={'font-weight': 'bold', 'padding-right': '12px'}),
                dcc.Input(id=c.NMC_INPUT_ID, type='number', placeholder='Enter NMC%', min=0, max=100)
            ]),
            html.Br(),
            html.Button("Submit", id=c.BUTTON_ID, n_clicks=0)
        ], id="form-box")
