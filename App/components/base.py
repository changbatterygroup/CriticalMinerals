from abc import ABC, abstractmethod
from dash.html import Div, Label
from dash.dcc import Slider
from common.constants import FormConfig as fc

class Component(ABC):
    
    
    @property
    @abstractmethod
    def layout(self)-> Div: 
        ...
        


