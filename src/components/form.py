from dash import html
from .base import Component


class FormComponent(Component):
    def __init__(self, fields):
        self.fields = fields

    def _generate_field_layout(self):
        for f in self.fields:
            yield f.to_layout()
            yield html.Br()
        
    @property
    def layout(self):
        return html.Div([
            html.H3("Mineral Reserves Over Time"),
            html.Br(),
            *self._generate_field_layout()
        ], id="form-box")

    def register_callbacks(self, app):
        for field in self.fields:
            field.get_callback(app)
            
