from dash import html, dcc, Input, Output, State
from common.constants import RESERVES_PLOT_ID
from Backend.plot import plot_reserves ,plot_reserves_and_demand
from App.components.base import Component
from common.constants import FormConfig as fc
import dash.exceptions


class ReservesComponent(Component):
    def __init__(self, reserves_data, capacity_data):
        self.reserves_data = reserves_data
        self.capacity_data = capacity_data
        
    @property    
    def layout(self):
        return html.Div([
            html.H3("Mineral Reserves Over Time"),
            dcc.Loading(
                dcc.Graph(id = RESERVES_PLOT_ID,
                          figure = plot_reserves(self.reserves_data)[0]     
                ),
            overlay_style={"visibility":"visible", "opacity": .5},
            )
        ])
        

    def register_callbacks(self, app):
        
        @app.callback(
             Output(RESERVES_PLOT_ID, 'figure'),
            [Input(fc.NMC.input_id, 'value'), 
             Input(fc.CATHODE_DROPDOWN_ID, 'value'),
             Input(fc.POROSITY.input_id, 'value'),
             Input(fc.PARTICLE_SIZE.input_id, 'value'),
             Input(fc.THICKNESS.input_id, 'value'),
             ]
        )
        def update_reserves_plot(nmc_percentage, type, por, radius, thickness):
            
            return plot_reserves_and_demand(self.reserves_data, 
                                            self.capacity_data, 
                                            nmc_percentage, 
                                            type,
                                            por,
                                            radius,
                                            thickness
                                            )



