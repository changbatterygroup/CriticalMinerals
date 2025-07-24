from dash import Dash, html
from .components.form import FormComponent
from .components.reserves import ReservesComponent
from . import DataLoader
from core.configs.form_config import get_fields

body_components = [
    FormComponent(fields=get_fields()),
    ReservesComponent(DataLoader.get('cumulative_reserves'), DataLoader.get('capacity'))
]


class MainApp:
    
    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[
            'https://codepen.io/chriddyp/pen/bWLwgP.css',
        ])
        
        self.server = self.app.server

        
        # Layout
        self.app.layout = html.Div([
            html.H1("Critical Minerals Assessments"),
            html.P("This dashboard analyzes critical mineral reserves and battery material demand."),
            html.Br(),
            
            html.Div([x.render(self.app) for x in body_components], 
                     style={
                            "display": "flex",
                            "flexDirection": "row",
                            "gap": "10px"
                        }
            )
        ])

    
    def run(self, port):
        self.server.run(debug=True, port=port)

if __name__ == '__main__':
    app = MainApp()
    app.run(port=9342)