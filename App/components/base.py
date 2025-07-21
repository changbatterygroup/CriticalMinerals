from abc import ABC, abstractmethod
from dash.html import Div

class Component(ABC):
    
    @property
    @abstractmethod
    def layout(self)-> Div: 
        ...
        
    def render(self, app):
        self.register_callbacks(app)
        return self.layout
    
    @abstractmethod    
    def register_callbacks(self, app):
        ...
        


