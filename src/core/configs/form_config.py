from dataclasses import dataclass
from typing import Optional, Tuple
from dash.html import Div, Label
from dash.dcc import Slider
from core.configs import ids as c


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
        return  Div([
                Label(id=self.label_id ,style={'font-weight': 'bold', 'padding-right': '12px'}),
                Slider(id=self.input_id,
                           min=minimum, 
                           max=maximum, 
                           step = self.step, 
                           value=self.default_value, 
                           marks={i: str(i) for i in range(minimum, maximum + 1, self.marker_step)}),
                ])
    

def get_fields():
        return [

        FormFields(
            input_id=c.POROSITY_INPUT_ID,
            label_id=c.POROSITY_LABEL_ID,
            val_range=(10, 30),
            step=2,
            marker_step=5,
            default_value=15,
            label_format="Porosity: {}%"
        ),  

        FormFields(
            input_id=c.THICKNESS_INPUT_ID,
            label_id=c.THICKNESS_LABEL_ID,
            val_range=(50, 120),
            step=5,
            marker_step=10,
            default_value=50,
            label_format="Thickness: {} µm"
        ),

        FormFields(
            input_id=c.PARTICLE_SIZE_INPUT_ID,
            label_id=c.PARTICLE_SIZE_LABEL_ID,
            val_range=(10, 20),
            step=5,
            marker_step=5,
            default_value=15,
            label_format="Particle Size: {} µm radius"
        )
    ]

    