from dash import Dash, html
from .components.form import FormComponent
from .components.reserves import ReservesComponent
from . import DataLoader
from typing import List

class MainApp:
    
    def __load_data(self):
        self.reserves_data = DataLoader.get('cumulative_reserves')
        self.capacity_data = DataLoader.get('capacity')
        

    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[
            'https://codepen.io/chriddyp/pen/bWLwgP.css',
        ])
        
        self.server = self.app.server

        # Load data
        self.__load_data()

        # Initialize components
        self.form = FormComponent()
        self.reserves = ReservesComponent(self.reserves_data, self.capacity_data)
        
        # Layout
        self.app.layout = html.Div([
            html.H1("Critical Minerals Assessments"),
            html.P("This dashboard analyzes critical mineral reserves and battery material demand."),
            html.Br(),
            
            html.Div([
                self.form.render(self.app),
                self.reserves.render(self.app),
            ], style={
                    "display": "flex",
                    "flexDirection": "row",  # use "column" for vertical layout
                    "gap": "10px"
                }
            )
        ])

    
    def run(self, port):
        self.server.run(debug=True, port=port)

if __name__ == '__main__':
    app = MainApp()
    app.run(port=9342)