
import pybamm
import numpy as np
from backend.schema import Cathode, DemandParams
from logger import logger


class DemandCalculator:
    def __init__(self, cathode: Cathode, template: pybamm.ParameterValues):
        self.cathode = cathode
        self.template = template


    def get_avg_voltage(self, time, inputs: DemandParams):
        self.template.update(inputs.sim_params())
        self.template["Current function [A]"] = 0.5

        solver = pybamm.IDAKLUSolver(rtol=1e-3, atol=1e-4)
        sim = pybamm.Simulation(
            model=pybamm.lithium_ion.DFN(),
            parameter_values=self.template,
            solver=solver
        )

        sol = sim.solve(time, initial_soc=0.4, showprogress=True)
        return sol["Voltage [V]"].data.mean()

    def active_mass_calc(self, gwh, voltage):
        gwh = np.array(gwh)
        masses = ((gwh[:, None] * 1e3) / (voltage * self.cathode.capacity) * self.cathode.composition).T
        return masses

    def run(self, gwh, time, inputs):
        logger.info("Simulating with %s", inputs)
        voltage = self.get_avg_voltage(time, inputs)
        res = self.active_mass_calc(gwh, voltage)
        logger.info("Done")

        return res




   
