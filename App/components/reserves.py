from dash import html, dcc, Input, Output, State
from App.constants import RESERVES_PLOT_ID, NMC_INPUT_ID, BUTTON_ID
from Backend.Plotting.ReservesPlotter import ReservesPlotter
from Backend.Plotting.DemandPlotter import DemandPlotter
from App.components.base import *
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
        @app.callback(
            Output(RESERVES_PLOT_ID, 'figure'),
            [State(NMC_INPUT_ID, 'value')],
            Input(BUTTON_ID, 'n_clicks'),
            prevent_initial_callbacks=True
        )
        def update_reserves_plot(nmc_percentage, n_clicks):
            if n_clicks is None or nmc_percentage is None:
                raise dash.exceptions.PreventUpdate
            demand_plotter = DemandPlotter(self.capacity_data, self.reserves_plotter)
            return demand_plotter.plot(nmc_percentage)
