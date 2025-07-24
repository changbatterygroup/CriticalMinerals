from dash import html, dcc, Input, Output
import core.ids as c
from Backend.plot import plot_reserves, add_demand_traces
from core.schema import DemandParams
from .base import Component
from core.configs.cathode_config import CATHODE_SPECS

class ReservesComponent(Component):
    def __init__(self, reserves_data, capacity_data):
        self.reserves_data = reserves_data
        self.capacity_data = capacity_data
        
    @property    
    def layout(self):
        return html.Div([
            dcc.Loading(
                dcc.Graph(id = c.RESERVES_PLOT_ID,
                          figure = plot_reserves(self.reserves_data)[0]     
                ),
            overlay_style={"visibility":"visible", "opacity": .5},
            type="circle"
            )
        ],  style={"flex": "2"})
        

    def register_callbacks(self, app):
        @app.callback(
             Output(c.RESERVES_PLOT_ID, 'figure'),
             [Input(c.CATHODE_DROPDOWN_ID, 'value'),
              Input(c.POROSITY_INPUT_ID, "value"),
              Input(c.PARTICLE_SIZE_INPUT_ID, "value"),
              Input(c.THICKNESS_INPUT_ID, "value")
            ]

        )
        def update_reserves_plot(cathode, por, radius, thickness):
            category = CATHODE_SPECS.get("cathode", {}).get("category")
            fig, minerals_used, subplot_domains = plot_reserves(self.reserves_data)
            params = DemandParams.scaled(por, radius, thickness)
            add_demand_traces(fig, self.capacity_data, minerals_used, subplot_domains,
                              category, cathode, params)

            return fig






