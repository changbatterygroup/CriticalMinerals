import numpy as np
import pybamm
from abc import ABC, abstractmethod
from Backend.DemandCalculator import DemandCalculator


class Calculator(ABC):
    @abstractmethod
    def calculate(self, *args, **kwargs):
        pass


class Model(Calculator):
    
    def __init__(self, param_template: pybamm.ParameterValues, model=None, solver=None):
        self._model = model or pybamm.lithium_ion.DFN()
        self._param_set =  param_template
        self._solver = solver or pybamm.IDAKLUSolver()
        
    def __define_geom(self, params):
        self._param_set.update(params)

    def calculate(self, time, por, radius, thickness):
        inputs = {"Positive electrode porosity": '[input]'}
        
        self.__define_geom({
            "Positive particle radius [m]": radius,
            "Positive electrode thickness [m]": thickness,
        })
        self._param_set.update(inputs)
        model = pybamm.lithium_ion.DFN()
        sim = pybamm.Simulation(model=model, parameter_values=self._param_set, solver=self._solver)
        soln = sim.solve(time, inputs={"Positive electrode porosity": por}, initial_soc=0.5)
        return soln["Voltage [V]"].data.mean()


    
 

class ModelFactory:
    
    def create(self, model_type):
        if model_type.lower() == "lfp":
            params = pybamm.ParameterValues("Prada2013")
            
            return Model(params)
                
        elif model_type.lower() == "nmc":
            params = pybamm.ParameterValues("Chen2020")
            return Model(params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
 
   
if __name__ == "__main__":
    import pandas as pd
    import os, sys
    

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    
    
    data = pd.read_parquet("Assets/Capacity.parquet")
    por, radius, thickness = 0.3, 15e-6, 50e-6  # Porosity, radius, thickness in meters
    


    nmc_model = ModelFactory().create("nmc")
    lfp_model = ModelFactory().create("lfp")


    v = []
    for porosity in [0.15, 0.30]:
        avg_v = nmc_model.calculate([0, 3600], porosity, radius, thickness)
        v.append(avg_v)


    c = DemandCalculator()
    for a_v in v:
        x = c.AM_calc(data['Capacity'] * 0.8, a_v, "NMC811")
        
        
        print(x[1])
        print()