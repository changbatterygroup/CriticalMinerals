from dash import html, dcc, Input, Output
import core.ids as c
from backend.plot import ReservesPlot
from backend.schema import DemandParams, Result
from backend.factory import CalculatorFactory
from .base import Component
import numpy as np
from core.cathode_config import CATHODE_SPECS, CATHODE_MODEL_TEMPLATES
from pandas import Series


class ReservesComponent(Component):
    def __init__(self, reserves_data, capacity_data):
        self.reserves_data = reserves_data
        self.capacity_data = capacity_data
        self.base = ReservesPlot.Builder(self.reserves_data, self.capacity_data)

    @property    
    def layout(self):
        return html.Div([
            dcc.Loading(
                dcc.Graph(id = c.RESERVES_PLOT_ID,figure = self.base.add_reserves().plot()),
            overlay_style={"visibility":"visible", "opacity": .5},
            type="circle"
            )
        ])
        

    def register_callbacks(self, app):

        calc = CalculatorFactory(CATHODE_SPECS, CATHODE_MODEL_TEMPLATES)
        t = np.linspace(0, 3600, 100+1)
        default = Series(1, index=self.capacity_data.index)

        def calculate(time, inputs: DemandParams) -> Result:
            total_demand = 0
            for i, (cathode, data) in enumerate(CATHODE_SPECS.items()):
                model = calc.create(cathode)
                res = model.run(self.capacity_data["Capacity"], time, inputs)
                breakdown = self.capacity_data.get(data.get('category'), default)
                total_demand += res * breakdown.to_numpy()


            return Result(*total_demand)


        @app.callback(
             Output(c.RESERVES_PLOT_ID, 'figure'),
             [Input(c.POROSITY_INPUT_ID, "value"),
              Input(c.PARTICLE_SIZE_INPUT_ID, "value"),
              Input(c.THICKNESS_INPUT_ID, "value")
            ]

        )
        def update_reserves_plot(por, radius, thickness):
            trace_map = calculate(t, DemandParams.scale(por, radius, thickness))

            fig = (self.base
                   .reset()
                   .add_reserves()
                   .add_current_year_marker(2024)
                   .initialize_insets()
                   .add_demand_traces(trace_map.to_dict())
                   .update_inset_traces()
                   .plot())
            return fig


