from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Self
import numpy as np


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


@dataclass
class DemandParams:
    porosity: float
    radius: float
    thickness: float

    @classmethod
    def scaled(cls, porosity_pct, radius_um, thickness_um):
        return cls(
            porosity=porosity_pct / 100,
            radius=radius_um * 1e-6,
            thickness=thickness_um * 1e-6
        )

@dataclass
class Cathode(FromConfigMixin):

    name: str
    capacity: float
    composition: np.ndarray | List
    category: str = ""

    def __post_init__(self):
        self.composition = np.array(self.composition)

    @classmethod
    def _from_spec(cls, name, spec):
        return cls(
            name=name,
            capacity=spec.get("capacity", 0),
            composition=spec.get("composition", []),
            category = spec.get("category", "")
        )