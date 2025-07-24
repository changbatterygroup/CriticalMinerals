
import pybamm
import numpy as np
from core.configs.cathode_config import CATHODE_SPECS
from core.schema import FromConfigMixin, Cathode
from logger import logger




class Model(FromConfigMixin):
    
    def __init__(self, param_template: pybamm.ParameterValues, solver=None):
        self._param_set =  param_template
        self._solver = solver or pybamm.IDAKLUSolver(atol=1e-5, rtol=1e-3)
        
    @classmethod
    def _from_spec(cls, name, spec):
        template = spec.get('template')
        
        if template is None:
            raise ValueError(f"No suitable model found for {name}")
        
        logger.info(f"Got model: {template} for {name}")
  
        return cls(pybamm.ParameterValues(template))
    
    
    def _define_geom(self, params):
        self._param_set.update(params)

    def simulate(self, time, por, radius, thickness):
        inputs = {"Positive electrode porosity": '[input]'}
        
        self._define_geom({
            "Positive particle radius [m]": radius,
            "Positive electrode thickness [m]": thickness,
        })
        self._param_set.update(inputs)

        sim = pybamm.Simulation(model=pybamm.lithium_ion.DFN(), parameter_values=self._param_set, solver=self._solver)
        soln = sim.solve(time, inputs={"Positive electrode porosity": por}, initial_soc=0.6, showprogress=True)
        return soln["Voltage [V]"].data.mean()







class DemandCalculator:
    
    def __init__(self, cathode: Cathode, model: Model):
        self.cathode = cathode
        self.model = model
    
    @classmethod
    def from_config(cls, name, config=CATHODE_SPECS):
        cathode = Cathode.from_config(name, config)
        model = Model.from_config(name, config)
        return cls(cathode, model)
        
  
     
    def AM_calc(self, gwh, voltage):
        gwh = np.array(gwh)
        return ((gwh[:, None] * 1e3) / (voltage * self.cathode.capacity) * self.cathode.composition).T
    

    def run(self, gwh, time, por, radius, thickness):
        logger.info("Simulating")
        voltage = self.model.simulate(time, por, radius, thickness)
        gwh = np.array(gwh)

        demand = self.AM_calc(gwh, voltage)

        logger.info("Done")
        return demand



if __name__ == '__main__':
    import pandas as pd

    t2 = "NCA"
    
    por = 15
    radius = 15
    thickness = 50
    
    
    # ------------------------------------------------------------------------------------
    capacity_df = pd.read_parquet("./Assets/Capacity.parquet")
    needed_nmc = capacity_df["Capacity"] * capacity_df[CATHODE_SPECS[t2]['category']]
    needed_lfp = capacity_df["Capacity"] * capacity_df[CATHODE_SPECS['LFP']['category']]
    
    logger.debug("Got DF: \n%s",capacity_df)
    lfp_model = DemandCalculator.from_config("LFP")
    t2_model = DemandCalculator.from_config(t2)
    

    t = np.linspace(0, 3600, 100)
    total = lfp_model.run(needed_lfp, t, por / 100, radius * 1e-6, thickness * 1e-6)
    if t2 != "LFP":
        total +=  t2_model.run(needed_nmc, t, por / 100, radius * 1e-6, thickness * 1e-6)

    
    logger.debug("Result: \n%s", total)
   
   
