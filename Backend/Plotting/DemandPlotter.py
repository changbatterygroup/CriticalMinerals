
import plotly.graph_objects as go
from Backend.DemandCalculator import DemandCalculator
from Backend.Plotting import Plotter
from Backend.Model import ModelFactory


class DemandPlotter(Plotter):
    def __init__(self, data, reserves_plotter) -> None:
        super().__init__(data)
        self.reserve_p = reserves_plotter
        self.calc = DemandCalculator()
        factory = ModelFactory()
        self.nmc_model = factory.create("nmc")
        self.lfp_model = factory.create("lfp")

    
    def plot(self, nmc_percentage, type, por, radius, thickness):
        self.fig = self.reserve_p.plot()
        
        traces = self.get_traces(nmc_percentage / 100, type, por, radius, thickness)
        
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
        

    def get_traces(self, pct_nmc, nmc_cathode_type, por, radius, thickness):
        needed_nmc = self.data['Capacity'] * pct_nmc
        needed_lfp = self.data['Capacity'] * (1 - pct_nmc)
        
        inputs={
            "Positive electrode porosity": por,
            "Positive particle radius [m]": radius * 1e-6,
            "Positive electrode thickness [m]": thickness * 1e-6,
        }

        lfp_voltage = self.lfp_model.calculate([0, 3600], inputs=inputs)
        nmc_voltage = self.nmc_model.calculate([0, 3600], inputs=inputs)
        
        
        LFP_Li = self.calc.AM_calc(needed_lfp, lfp_voltage, "LFP")[0]
        NMC_Li, Ni_mass, Mn_mass, Co_mass = self.calc.AM_calc(needed_nmc, nmc_voltage, nmc_cathode_type)
        total_Li = LFP_Li + NMC_Li

        traces = [
            go.Scatter(x=self.data['Year'], 
                       y=Co_mass, mode='lines+markers', 
                       name='Cobalt', line=dict(color='darkorange'), showlegend=False),
            go.Scatter(x=self.data['Year'], 
                       y=total_Li, mode='lines+markers', 
                       name='Lithium', 
                       line=dict(color='royalblue'),
                       showlegend=False),
            go.Scatter(x=self.data['Year'], 
                       y=Ni_mass, mode='lines+markers',
                       name='Nickel', 
                       line=dict(color='gold'),
                       showlegend=False),
            go.Scatter(x=self.data['Year'], 
                       y=Mn_mass, 
                       mode='lines+markers', 
                       name='Manganese', 
                       line=dict(color='yellowgreen'),
                       showlegend=False),
        
        ]
        return traces