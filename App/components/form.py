
from dash import html, dcc, Input, Output, State
from common.constants import CAPACITIES
from common.constants import FormConfig as fc
from App.components.base import StaticComponent, FunctionalComponent




class FormComponent(FunctionalComponent):
    def __init__(self):
        cathodes = list(CAPACITIES.keys())
        
        self.layout = html.Div([
            dcc.Dropdown(id=fc.CATHODE_DROPDOWN_ID, options=cathodes[:-2], value=cathodes[0], clearable=False),
            html.Br(),
            html.Div([
                html.Label(id=fc.NMC.label_id ,style={'font-weight': 'bold', 'padding-right': '12px'}),
                dcc.Slider(id=fc.NMC.input_id, 
    
                           min=fc.NMC.val_range[0], 
                           max=fc.NMC.val_range[1], 
                           step = fc.NMC.step, 
                           value=fc.NMC.default_value, 
                           marks={
                    i: str(i) for i in range(fc.NMC.val_range[0], fc.NMC.val_range[1] + 1, 25)}),
                
            ]),
            html.Br(),
            html.Div([
                html.Label(id=fc.POROSITY.label_id, 
                           style={'font-weight': 'bold', 'padding-right': '10px'}
                           ),
                dcc.Slider(
                           id=fc.POROSITY.input_id, 

                           min=fc.POROSITY.val_range[0], 
                           max=fc.POROSITY.val_range[1], 
                           step = fc.POROSITY.step, 
                           value=fc.POROSITY.default_value,
                           marks={
                    i: str(i) for i in range(fc.POROSITY.val_range[0], fc.POROSITY.val_range[1]+1, 10)
                    })
            ]),
            html.Br(),
            html.Div([
                html.Label(id=fc.THICKNESS.label_id, 
                           style={'font-weight': 'bold', 'padding-right': '10px'}),
                dcc.Slider(id=fc.THICKNESS.input_id, 

                           min=fc.THICKNESS.val_range[0], 
                           max=fc.THICKNESS.val_range[1],
                           step = fc.THICKNESS.step,
                           value=fc.THICKNESS.default_value,
                           marks={
                    i: str(i) for i in range(fc.THICKNESS.val_range[0], fc.THICKNESS.val_range[1]+1, 10)
                    }
                    ) 
            ]),
            html.Br(),
            html.Div([
                html.Label(id=fc.PARTICLE_SIZE.label_id, 
                           style={'font-weight': 'bold', 'padding-right': '10px'}),
                dcc.Slider(id=fc.PARTICLE_SIZE.input_id,
                            
                           min=fc.PARTICLE_SIZE.val_range[0], 
                           max=fc.PARTICLE_SIZE.val_range[1],
                           step = fc.PARTICLE_SIZE.step,
                           value=fc.PARTICLE_SIZE.default_value,
                    ) 
            ]),
            
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
            return f"Porosity: {porosity} µm"
        

        
        @app.callback(
            Output(fc.PARTICLE_SIZE.label_id, 'children'),
            Input(fc.PARTICLE_SIZE.input_id, 'value'),
        )
        def update_particle_size(particle_size):
            return f"Particle Size: {particle_size} µm radius"