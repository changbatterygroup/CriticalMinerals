
import pybamm
from abc import ABC, abstractmethod
from typing import List, Self
import numpy as np
from dataclasses import dataclass
from core.constants import CATHODE_SPECS
from logger import logger

class FromConfigMixin(ABC):
    
    @classmethod
    def from_config(cls, name: str, config: dict):
        spec = config.get(name)
        if spec is None:
            raise ValueError(f"No config found for {name}")
        return cls._from_spec(name, spec)

    @classmethod
    @abstractmethod
    def _from_spec(cls, name: str, spec: dict)->Self:
        pass



class Model(FromConfigMixin):
    
    def __init__(self, param_template: pybamm.ParameterValues, solver=None):
        self._param_set =  param_template
        self._solver = solver or pybamm.IDAKLUSolver(atol=1e-6, rtol=1e-4)
        
    @classmethod
    def _from_spec(cls, name, spec):
        template = spec.get('template')
        
        if template is None:
            raise ValueError(f"No suitable model found for {name}")
        
        logger.info(f"Got model: {template} for {name}")
  
        return cls(pybamm.ParameterValues(template))
    
    
    def _define_geom(self, params):
        self._param_set.update(params)

    def calculate(self, time, por, radius, thickness):
        inputs = {"Positive electrode porosity": '[input]'}
        
        self._define_geom({
            "Positive particle radius [m]": radius,
            "Positive electrode thickness [m]": thickness,
        })
        self._param_set.update(inputs)
        
        logger.debug("Simulating")
        sim = pybamm.Simulation(model=pybamm.lithium_ion.DFN(), parameter_values=self._param_set, solver=self._solver)
        soln = sim.solve(time, inputs={"Positive electrode porosity": por}, initial_soc=0.6, showprogress=True)
        return soln["Voltage [V]"].data.mean()


@dataclass
class Cathode(FromConfigMixin):
    
    name: str
    capacity: float
    composition: np.ndarray | List
    
    def __post_init__(self):
        self.composition = np.array(self.composition)
        
    @classmethod
    def _from_spec(cls, name, spec):
        return cls(
            name=name,
            capacity=spec.get("capacity", 0),
            composition=spec.get("composition", [])
        )
            

class DemandCalculator:
    
    def __init__(self, cathode: Cathode, model: Model):
        self.cathode = cathode
        self.model = model
    
    @classmethod
    def from_config(cls, name, config=CATHODE_SPECS):
        cathode = Cathode.from_config(name, config)
        model = Model.from_config(name, config)
        return cls(cathode, model)
        
  
     
    def AM_calc(self, GWH, voltage):
        GWH = np.array(GWH)
        return ((GWH[:, None] * 1e3) / (voltage * self.cathode.capacity) * self.cathode.composition).T   
    

    def run(self, GWH, time, por, radius, thickness):
        voltage = self.model.calculate(time, por, radius, thickness)
        GWH = np.array(GWH)
        return self.AM_calc(GWH, voltage)



if __name__ == '__main__':
    import pandas as pd
    
    
    nmc_pct = 55
    t2 = "NCA"
    
    por = 15
    radius = 15
    thickness = 55
    
    
    # ------------------------------------------------------------------------------------
    capacity_df = pd.read_parquet("Assets/Capacity.parquet")
    needed_nmc = capacity_df["Capacity"] * (nmc_pct / 100)
    needed_lfp = capacity_df["Capacity"] * (1 - (nmc_pct / 100))
    
 
    # Suppose you have two models already built
    lfp_model = DemandCalculator.from_config("LFP")
    t2_model = DemandCalculator.from_config(t2)
    

    t = np.linspace(0, 3600, 100)
    total = lfp_model.run(needed_lfp, t, por / 100, radius * 1e-6, thickness * 1e-6)
    if t2 != "LFP":
        total +=  t2_model.run(needed_nmc, t, por / 100, radius * 1e-6, thickness * 1e-6)

    
    logger.info("Result: \n%s", total)
   
   
