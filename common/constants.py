from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, Dict



BUTTON_ID = 'submit_button'
BODY_ID = "placeholder"


CAPACITIES = {
            "NMC622": 0.180, 
            "NMC811": 0.200,
            "NMC532": 0.170,
            "NMC111": 0.160,
            "LFP":    0.120,
            "LCO":    0.140
            }
    



RESERVES_PLOT_ID = 'reserves-plot'


NMC = ["NMC622", "NMC811", "NMC532", "NMC111", "LIB"]

@dataclass
class FormFields:
    input_id: str
    label_id: str
    default_value: int
    val_range:  Tuple[int, int]
    step: Optional[float] = None



class FormConfig:
    CATHODE_DROPDOWN_ID = "cathode-dropdown"

    
    NMC = FormFields(
        input_id='nmc-input',
        label_id='NMC-label',
        val_range=(0, 100),
        step=5,
        default_value=50
    )
    
    
    POROSITY = FormFields(
        input_id='porosity-input',
        label_id='porosity-pct-label',
        val_range=(10, 30),
        step=2,
        default_value=25
    )
    
    THICKNESS = FormFields(
        input_id='thickness-input',
        label_id='thickness-pct-label',
        val_range=(50, 120),
        step=5,
        default_value=50
    )
    
    PARTICLE_SIZE = FormFields(
        input_id='particle-size-input',
        label_id='particle-size-label',
        val_range=(10, 20),
        step=5,
        default_value=15
    )
    
    

    


class DropDownOptions(Enum):
    NMC = "nmc"
    LIB = "lib"
    RESERVES_MAP = 'reserves_map'
    
