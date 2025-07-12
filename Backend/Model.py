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
        self._solver = solver or pybamm.CasadiSolver()
        
    def __define_geom(self, params):
        self._param_set.update(params)

    def calculate(self, time, por, radius, thickness):
        inputs = {"Positive electrode porosity": '[input]'}
        
        self.__define_geom({
            "Positive particle radius [m]": radius,
            "Positive electrode thickness [m]": thickness,
        })
        self._param_set.update(inputs)
        
        sim = pybamm.Simulation(model=self._model, parameter_values=self._param_set, solver=self._solver)
        soln = sim.solve(time, inputs={"Positive electrode porosity": por}, initial_soc=1)
        return soln["Voltage [V]"].data.mean()


    
 

class ModelFactory:
    
    def create(self, model_type):
        if model_type.lower() == "lfp":
            params = pybamm.ParameterValues("Prada2013")
            return Model(params, solver=pybamm.CasadiSolver(rtol=1e-3, atol=1e-5, dt_max=0.5,
                                                            return_solution_if_failed_early = True
                                                            ))
                
        elif model_type.lower() == "nmc":
            params = pybamm.ParameterValues("Chen2020")
            return Model(params, solver=pybamm.CasadiSolver(rtol=1e-3, atol=1e-5, dt_max=0.5, 
                                                            return_solution_if_failed_early = True
                                                            ))
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
 
   
