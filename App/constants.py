from enum import Enum


BUTTON_ID = 'submit_button'
CATHODE_DROPDOWN_ID = "cathode-dropdown"
BODY_ID = "placeholder"
P_INPUT_ID = 'porosity-input'
P_PCT_ID = 'porosity-pct-label'

NMC_INPUT_ID = 'nmc-input'
RESERVES_PLOT_ID = 'reserves-plot'
NMC_LABEL_ID = 'NMC-label'

NMC = ["NMC622", "NMC811", "NMC532", "NMC111", "LIB"]


class Form(Enum):
    CATHODE_DROPDOWN_ID = "cathode-dropdown"
    NMC_INPUT_ID = 'nmc-input'
    NMC_LABEL_ID = 'NMC-label'
    P_INPUT_ID = 'porosity-input'
    P_PCT = 'porosity-pct-label'
    



class DropDownOptions(Enum):
    NMC = "nmc"
    LIB = "lib"
    RESERVES_MAP = 'reserves_map'
    
