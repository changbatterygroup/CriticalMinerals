from dash import html, dcc, Input, Output
from . import ids as c
from .base import Component



class FormComponent(Component):
    def __init__(self, fields=[]):
        self.cathodes = c.CATHODE_OPTIONS
        self.fields = fields
        
    @property
    def layout(self):
        return html.Div([
            html.H3("Mineral Reserves Over Time"),
            dcc.Dropdown(id=c.CATHODE_DROPDOWN_ID, options=self.cathodes, value=self.cathodes[0], clearable=False),
            html.Br(),
            *[item for f in self.fields 
                   for item in (f.to_layout(), 
                                html.Br()
                                )
            ]
        ], style={"flex": "1", "width": "12%", "padding": "5px"}, id="form-box")

    def register_callbacks(self, app):
        
        for field in self.fields:
            app.callback(
            Output(field.label_id, 'children'),
            Input(field.input_id, 'value'),
            )(lambda value, t=field.label_format: t.format(value))
            
