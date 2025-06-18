from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def __init__(self):
        self.layout = None
    
    
class StaticComponent(Component, ABC):
    
    @abstractmethod
    def __init__(self):
        ...
        

class FunctionalComponent(Component, ABC):
    
    def __init__(self, *args):
        ...
    
    
    @abstractmethod
    def register_callbacks(self, app):
        ...
