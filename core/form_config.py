from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple
from dash import html, dcc



@dataclass
class FormFields:
    input_id: str
    label_id: str
    default_value: int
    val_range:  Tuple[int, int]
    step: Optional[int] = 1
    marker_step: int = step
    label_format: str = '{}'
    
    def format_label(self, value):
        return self.label_format.format(value)
    
    def to_layout(self):
        minimum, maximum = self.val_range
        return  html.Div([
                html.Label(id=self.label_id ,style={'font-weight': 'bold', 'padding-right': '12px'}),
                dcc.Slider(id=self.input_id, 
                           min=minimum, 
                           max=maximum, 
                           step = self.step, 
                           value=self.default_value, 
                           marks={i: str(i) for i in range(minimum, maximum + 1, self.marker_step)}),
                ])
    

class FormConfig:
    
    NMC = FormFields(
        input_id='nmc-input',
        label_id='NMC-label',
        val_range=(0, 100),
        step=5,
        marker_step=25,
        default_value=50,
        label_format="NMC Composition: {}%"
    )

    POROSITY = FormFields(
        input_id='porosity-input',
        label_id='porosity-pct-label',
        val_range=(10, 30),
        step=2,
        marker_step=5,
        default_value=15,
        label_format="Porosity: {}%"
    )

    THICKNESS = FormFields(
        input_id='thickness-input',
        label_id='thickness-pct-label',
        val_range=(50, 120),
        step=5,
        marker_step=10,
        default_value=50,
        label_format="Thickness: {} µm"
    )

    PARTICLE_SIZE = FormFields(
        input_id='particle-size-input',
        label_id='particle-size-label',
        val_range=(10, 20),
        step=5,
        marker_step=5,
        default_value=15,
        label_format="Particle Size: {} µm radius"
    )
    
    @property
    def fields(self):
        return [
            self.NMC,
            self.POROSITY,
            self.THICKNESS,
            self.PARTICLE_SIZE,
        ]

    