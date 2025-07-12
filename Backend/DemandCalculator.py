import numpy as np
from common.constants import CAPACITIES


class DemandCalculator():
    
    def __init__(self, elyte = 0.005863):
        self.elyte = elyte
        self.capacities = CAPACITIES

        
        self.compositions_arr = np.array([
            [0.07162 + elyte, 0.3634, 0.1134, 0.1216],
            [0.07136 + elyte, 0.4828, 0.05648, 0.06059],
            [0.07190 + elyte, 0.3040, 0.1707, 0.1221],
            [0.0328 + elyte,  0.2775, 0.2598, 0.2787],
            [0.044 + elyte,   0,      0,      0],
            [0.0709 + elyte,  0,      0,      0.602]
        ])
        
        self.compositions = {comp: self.compositions_arr[i] for i, comp in enumerate(self.capacities)}
        
    def AM_calc(self, GWh, voltage, type):
        GWH = np.array(GWh)  # convert to numpy array for element-wise operations
        if type not in self.capacities: 
            raise ValueError(f'{type} is an unsupported cathode at this time.')

        cap = self.capacities[type] # Ah/g
        elements = self.compositions[type] # wt% Li, Ni, Mn, Co
        return ((GWH[:, None] * 1e3) / (voltage * cap) * elements).T
    
    


