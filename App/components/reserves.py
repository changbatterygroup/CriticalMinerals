from dash import html, dcc, Input, Output, State
from App.constants import *
from Backend.Plotting.ReservesPlotter import ReservesPlotter
from Backend.Plotting.DemandPlotter import DemandPlotter
from App.components.base import *
from App.constants import FormConfig as fc
import dash.exceptions

class ReservesComponent(FunctionalComponent):
    def __init__(self, reserves_data, capacity_data):
        super().__init__()
        self.reserves_data = reserves_data
        self.capacity_data = capacity_data
        self.reserves_plotter = ReservesPlotter(self.reserves_data)
        self.layout = html.Div([
            html.H3("Mineral Reserves Over Time"),
            dcc.Graph(id=RESERVES_PLOT_ID, figure=self.reserves_plotter.plot())
        ])

    def register_callbacks(self, app):
        
        demand_plotter = DemandPlotter(self.capacity_data, self.reserves_plotter)
        
        
        @app.callback(
             Output(RESERVES_PLOT_ID, 'figure'),
            [Input(fc.NMC.input_id, 'value'), Input(fc.CATHODE_DROPDOWN_ID, 'value')],
        )
        def update_reserves_plot_by_nmc_pct(nmc_percentage, type):
            if nmc_percentage is None or type is None:
                raise dash.exceptions.PreventUpdate

            return demand_plotter.plot(nmc_percentage, type)



