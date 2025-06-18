from enum import Enum


BUTTON_ID = 'submit_button'
DROPDOWN_ID = "dropdown"
BODY_ID = "placeholder"
P_INPUT_ID = 'porosity-input'
NMC_INPUT_ID = 'nmc-input'
RESERVES_PLOT_ID = 'reserves-plot'

class DropDownOptions(Enum):
    NMC = "nmc"
    LIB = "lib"
    RESERVES_MAP = 'reserves_map'
    
