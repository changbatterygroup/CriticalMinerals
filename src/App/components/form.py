from dash import html, dcc, Input, Output
from core.configs import cathode_config as c, ids
from .base import Component



class FormComponent(Component):
    def __init__(self, fields):
        self.fields = fields
        
    @property
    def layout(self):
        return html.Div([
            html.H3("Mineral Reserves Over Time"),
            dcc.Dropdown(id=ids.CATHODE_DROPDOWN_ID, options=c.CATHODE_OPTIONS, value=c.CATHODE_DEFAULT, clearable=False),
            html.Br(),
            *[item for f in self.fields 
                   for item in (f.to_layout(), 
                                html.Br()
                                )
            ]
        ], id="form-box")

    def register_callbacks(self, app):
        
        for field in self.fields:
            app.callback(
            Output(field.label_id, 'children'),
            Input(field.input_id, 'value'),
            )(lambda value, t=field.label_format: t.format(value))
            
