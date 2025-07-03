import numpy as np
import pybamm
from abc import ABC, abstractmethod
from Backend.DemandCalculator import DemandCalculator


class Calculator(ABC):
    @abstractmethod
    def calculate(self, *args, **kwargs):
        pass


class Model(Calculator):
    
    def __init__(self, model=None, simulation=None):
        self._model = model or pybamm.lithium_ion.DFN()
        self._params: pybamm.ParameterValues
        self._solver = pybamm.CasadiSolver()
        self.simulation = simulation

    
    def calculate(self, time, inputs):
        
        if not self.simulation:
            raise ValueError("Simulation not initialized. Please build the model first.")
        soln = self.simulation.solve(time, inputs=inputs, initial_soc=0.1)
        return soln["Voltage [V]"].data.mean()


    
    class Builder():
        def __init__(self, model=None):
            self.model: Model = Model(model)
            

        def set_params(self, param_template, params=None):
            self.model._params = param_template
            if params is None:
                self.model._params.update(params)
            return self
        

        def set_solver(self, solver):
            self.model._solver = solver
            return self


        def build(self):
            self.model.simulation = pybamm.Simulation(
                model=self.model._model,
                parameter_values=self.model._params,
                solver=self.model._solver,
                
            )
            return self.model



class ModelFactory:
    
    def __init__(self):
        self.added_parameters = {
        "Current function [A]": 5,
        "Positive electrode porosity": "[input]",
        "Positive particle radius [m]": "[input]",
        "Positive electrode thickness [m]": "[input]",
    }   

    
    def create(self, model_type):
        if model_type.lower() == "lfp":
            return(Model.Builder()
                .set_params(param_template=pybamm.ParameterValues("Prada2013") ,
                            params=self.added_parameters)
                .set_solver(solver=pybamm.CasadiSolver(rtol=1e-6, atol=1e-4))
                .build()
                )
                
        elif model_type.lower() == "nmc":
            
            return (Model.Builder()
             .set_params(param_template=pybamm.ParameterValues("Chen2020"),
                         params=self.added_parameters)
             .build()
            )  
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
 
   
        

if __name__ == "__main__":
    import pandas as pd
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    
    
    data = pd.read_parquet("Assets/Capacity.parquet")
    por, radius, thickness = 0.25, 15e-6, 50e-6  # Porosity, radius, thickness in meters
    


    nmc_model = ModelFactory().create("nmc")
    lfp_model = ModelFactory().create("lfp")
    
     
    avg_v = nmc_model.calculate(
        time=np.linspace(0,3600, 200),
        inputs={
            "Positive electrode porosity": por,
            "Positive particle radius [m]": radius,
            "Positive electrode thickness [m]": thickness,
        })

    c = DemandCalculator()
    x = c.AM_calc(data['Capacity'].values, avg_v, "NMC811")
    print(x)