from dataclasses import dataclass
from typing import List, Dict

import numpy as np

from core.cathode_config import CURRENT


@dataclass
class Result:
    lithium: np.ndarray
    cobalt: np.ndarray
    manganese: np.ndarray
    nickel: np.ndarray


@dataclass
class Cathode:
    name: str
    capacity: float
    composition: np.ndarray | List
    category: str = ""

    def __post_init__(self):
        self.composition = np.array(self.composition)

    @classmethod
    def from_spec(cls, spec: dict, name=None):
        return Cathode(
            name=name or spec.get("name", ""),
            capacity=spec.get("capacity", 0),
            composition=spec.get("composition", []),
            category=spec.get("category", "")
        )


@dataclass
class DemandParams:
    porosity: float
    thickness: float
    radius: float
    current: float = CURRENT

    @classmethod
    def scale(cls, porosity, thickness, radius):
        return cls(
            porosity=porosity / 100,
            thickness=thickness * 1e-6,
            radius = radius * 1e-6,
        )

    def sim_params(self) -> Dict[str, float]:
        """Convert to dictionary for simulation parameters"""
        return {
            "Current function [A]": self.current,
            "Positive electrode porosity": self.porosity,
            "Positive particle radius [m]": self.radius,
            "Positive electrode thickness [m]": self.thickness
        }

