import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Backend.Plotting import Plotter

class ReservesPlotter(Plotter):
    """Handles plotting of mineral reserves over time"""
    
    def __init__(self, data):
        super().__init__(data)
    
    def plot(self):
        """Create reserves over time plot"""
        minerals = self.data["Primary Mineral"].unique()
        self.fig = make_subplots(
            rows=2, cols=2, 
            x_title="Year", 
            y_title="Reserves", 
            subplot_titles=minerals.tolist()
        )
        
        for i, mineral in enumerate(minerals):
            mineral_data = self.data[self.data["Primary Mineral"] == mineral]
            row, col = i // 2 + 1, i % 2 + 1
            
            # Add main trace
            self.fig.add_trace(
                go.Scatter(
                    x=mineral_data["Year"],
                    y=mineral_data["Cumulative Reserves"],
                    mode="lines+markers",
                    legendgroup=mineral,
                    name=mineral,
                    marker=dict(size=10, color="black"),
                    showlegend=True,
                    legend="legend1"
                ),
                row=row, col=col
            )
            
            # Add current year marker
            self.add_current_year_marker(self.fig, row=row, col=col)
        
        self.fig.update_yaxes(type='log')
        self.fig.update_layout(
            title="Cumulative Growth in Reserves Over the Years",
            height=700,
            showlegend=True,
            legend1=dict(title=dict(text="Mineral"))
        )
        self.fig.update_annotations(font_size=20)
        
        return self.fig
    
    
    @staticmethod
    def add_current_year_marker(fig, year=2024, row=None, col=None):
        """Add a vertical line marking the current year"""
        fig.add_vline(x=year, line_dash="dash", line_color="red", row=row, col=col)
        fig.add_annotation(
            x=year,
            text="Current Year",
            showarrow=True,
            arrowhead=2,
            yshift=10,
            row=row,
            col=col
        )