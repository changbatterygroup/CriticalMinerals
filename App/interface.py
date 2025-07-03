# App/app.py

from dash import Dash, html
from App.components.form import FormComponent
from App.components.reserves import ReservesComponent
from Backend.DataLoader import DataLoader

class MainApp:
    
    def __load_data(self):
        self.reserves_data = DataLoader.get('cumulative_reserves')
        self.capacity_data = DataLoader.get('capacity')
       
        
    
    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[
            'https://codepen.io/chriddyp/pen/bWLwgP.css'
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
                html.Div(self.form.layout, style={'flex': '0.5'}),
                html.Div(self.reserves.layout, style={'flex': '1'}),
            ], style={
                    'display': 'flex',
                    'width': '100%',
                    'align-items': 'flex-start',
                    'justify-content': 'space-between',
                    'gap': '20px'
              })

        ])

        # Register all component callbacks
        self.form.register_callbacks(self.app)
        self.reserves.register_callbacks(self.app)

    def run(self, port):
        self.server.run(debug=True, port=port)

if __name__ == '__main__':
    app = MainApp()
    app.run(port=9342)