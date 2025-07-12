
from dash import html, dcc, Input, Output, State
from common.constants import CAPACITIES
from common.constants import FormConfig as fc
from App.components.base import *


class FormComponent(Component):
    def __init__(self):
        self.cathodes = list(CAPACITIES.keys())

    
    def __build_slider_input(self, f, marker_step: int=1):
        minimum, maximum = f.val_range
        return html.Div([
                html.Label(id=f.label_id ,style={'font-weight': 'bold', 'padding-right': '12px'}),
                dcc.Slider(id=f.input_id, 
                           min=minimum, 
                           max=maximum, 
                           step = f.step, 
                           value=f.default_value, 
                           marks={i: str(i) for i in range(minimum, maximum + 1, marker_step)}),
                ])
        
        
    @property
    def layout(self):
        return html.Div([
            dcc.Dropdown(id=fc.CATHODE_DROPDOWN_ID, options=self.cathodes[:-2], value=self.cathodes[0], clearable=False),
            html.Br(),
            self.__build_slider_input(fc.NMC, 25),
            html.Br(),
            self.__build_slider_input(fc.POROSITY, 5),
            html.Br(),
            self.__build_slider_input(fc.THICKNESS, 10),
            html.Br(),
            self.__build_slider_input(fc.PARTICLE_SIZE, 5),
            
        ], id="form-box")

    def register_callbacks(self, app):
        @app.callback(
            Output(fc.NMC.label_id, 'children'),
            Input(fc.NMC.input_id, 'value'),
        )
        def update_nmc(nmc_percentage):
            return f"NMC Composition: {nmc_percentage}%"
        
        
        @app.callback(
            Output(fc.THICKNESS.label_id, 'children'),
            Input(fc.THICKNESS.input_id, 'value'),
        )
        def update_thickness_label(thickness):
            return f"Thickness: {thickness} µm"
        
        
        @app.callback(
            Output(fc.POROSITY.label_id, 'children'),
            Input(fc.POROSITY.input_id, 'value'),
        )
        def update_porosity(porosity):
            return f"Porosity: {porosity} %"
        
        @app.callback(
            Output(fc.PARTICLE_SIZE.label_id, 'children'),
            Input(fc.PARTICLE_SIZE.input_id, 'value'),
        )
        def update_particle_size(particle_size):
            return f"Particle Size: {particle_size} µm radius"