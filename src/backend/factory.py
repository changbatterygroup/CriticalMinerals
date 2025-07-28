from pybamm import ParameterValues
from .calculator import DemandCalculator
from .schema import Cathode


class CalculatorFactory:
    def __init__(self, cathode_specs: dict, model_templates: dict):
        self.cathode_specs = cathode_specs
        self.model_templates = model_templates


    def create(self, name: str) -> "DemandCalculator":
        # Get cathode config
        cathode_spec = self.cathode_specs.get(name)
        if cathode_spec is None:
            raise ValueError(f"No cathode spec found for '{name}'")

        # Get model template config
        model_template = self.model_templates.get(name)
        if model_template is None:
            raise ValueError(f"No model template found for '{name}'")

        # Build objects
        cathode = Cathode.from_spec(cathode_spec, name)
        parameters = ParameterValues(model_template)


        return DemandCalculator(cathode, parameters)