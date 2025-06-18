from abc import ABC, abstractmethod


class Plotter(ABC):
    
    def __init__(self, data):
        self.data = data
        self.fig = None
        
    
    @abstractmethod
    def plot(self, *args, **kwargs):
        pass
    
    def get_figure(self):
        return self.fig
    
    
    