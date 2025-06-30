import numpy as np
import plotly.graph_objects as go
from Backend.DemandCalculator import DemandCalculator
from Backend.Plotting import Plotter



class DemandPlotter(Plotter):
    def __init__(self, data, reserves_plotter) -> None:
        super().__init__(data)
        self.reserve_p = reserves_plotter
        self.calc = DemandCalculator()

    
    def plot(self, nmc_percentage, type):
        self.fig = self.reserve_p.plot()
        
        traces = self.get_traces(nmc_percentage / 100, type, 3.5)
        
        # Map traces to subplots based on mineral name
        mineral_subplot_map = {
            'Cobalt': (1, 1),
            'Lithium': (1, 2), 
            'Nickel': (2, 1),
            'Manganese': (2, 2)
        }
        
        for trace in traces:
            if trace.name in mineral_subplot_map:
                row, col = mineral_subplot_map[trace.name]
                self.fig.add_trace(trace, row=row, col=col)
        return self.fig
        

    def get_traces(self, pct_nmc, nmc_cathode_type, voltage=3.5):
        needed_nmc = self.data['Capacity'] * pct_nmc
        needed_lfp = self.data['Capacity'] * (1 - pct_nmc)

        LFP_Li = self.calc.AM_calc(needed_lfp, voltage, "LFP")[0]
        NMC_Li, Ni_mass, Mn_mass, Co_mass = self.calc.AM_calc(needed_nmc, voltage, nmc_cathode_type)
        total_Li = LFP_Li + NMC_Li

        traces = [
            go.Scatter(x=self.data['Year'], y=Co_mass, mode='lines+markers', name='Cobalt', line=dict(color='darkorange')),
            go.Scatter(x=self.data['Year'], y=total_Li, mode='lines+markers', name='Lithium', line=dict(color='royalblue')),
            go.Scatter(x=self.data['Year'], y=Ni_mass, mode='lines+markers', name='Nickel', line=dict(color='gold')),
            go.Scatter(x=self.data['Year'], y=Mn_mass, mode='lines+markers', name='Manganese', line=dict(color='yellowgreen')),
        
        ]
        return traces