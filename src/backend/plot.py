import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ReservesPlot:

    def __init__(self, reserves_df, capacity_df):
        self.reserves_df = reserves_df
        self.capacity_df = capacity_df
        self.minerals = self.reserves_df["Primary Mineral"].unique().tolist()
        self.fig = go.Figure()


    class Builder:
        def __init__(self, reserves_df, capacity_df):
            self.p = ReservesPlot(reserves_df, capacity_df)
            self._init_plot()
            self.inset_axes = {}
            self.color_map = {
                "Cobalt": "darkorange",
                "Lithium": "royalblue",
                "Nickel": "purple",
                "Manganese": "yellowgreen",
            }

        def _init_plot(self):
            self.p.fig = make_subplots(rows=2, cols=2, x_title="Year",  y_title="Reserves", subplot_titles=self.p.minerals)
            self.inset_axes = {}
            self.p.fig.update_yaxes(type="log")
            self.p.fig.update_annotations(font_size=20)
            self.p.fig.update_layout(
                title="Cumulative Growth in Reserves vs Demand Over the Years",
                height=700,
                showlegend=True,
                legend=dict(title=dict(text="Mineral")),
            )
            return self

        def reset(self):
            self._init_plot()

            return self


        def add_reserves(self):
            for i, mineral in enumerate(self.p.minerals):
                mineral_data = self.p.reserves_df[self.p.reserves_df["Primary Mineral"] == mineral]
                self.inset_axes[mineral] = {}
                row, col = i // 2 + 1, i % 2 + 1

                self.p.fig.add_trace(
                    go.Scatter(
                        x=mineral_data["Year"],
                        y=mineral_data["Cumulative Reserves"],
                        mode="lines+markers",
                        legendgroup=mineral,
                        name=mineral,
                        marker=dict(size=10, color="black"),
                        showlegend=True,
                        legend="legend1",
                    ),
                    row=row,
                    col=col,
                )



            return self

        def add_current_year_marker(self, year=2024):
            annotation = go.layout.Annotation(
                x=year,
                text="Current Year",
                showarrow=True,
                arrowhead=2,
                ax=-30,
            )
            self.p.fig.add_vline(x=year, line_dash="dash", line_color="red", annotation=annotation ,
                                 annotation_position="bottom left")
            return self

        def initialize_insets(self):
            subplot_domains = {}
            for i, mineral in enumerate(self.p.minerals):

                row, col = i // 2 + 1, i % 2 + 1
                subplot_domains[(row, col)] = {
                    "x": self.p.fig.layout[f"xaxis{row * 2 + col - 2}"].domain,
                    "y": self.p.fig.layout[f"yaxis{row * 2 + col - 2}"].domain,
                }


                domain = subplot_domains[(row, col)]
                dx = domain["x"][1] - domain["x"][0]
                dy = domain["y"][1] - domain["y"][0]

                inset_width = min(dx * 0.21, 0.18)
                inset_height = min(dy * 0.25, 0.25)

                inset_x = np.array([domain["x"][0] + dx * 0.75, domain["x"][0] + dx * 0.75 + inset_width])
                inset_y = np.array([domain["y"][0] + dy * 0.12, domain["y"][0] + dy * 0.12 + inset_height])

                inset_id = 5 + row * 2 + col - 3  # unique axis ID
                xaxis_id = f"xaxis{inset_id}"
                yaxis_id = f"yaxis{inset_id}"
                inset_axis_name_x = f"x{inset_id}"
                inset_axis_name_y = f"y{inset_id}"


                self.inset_axes[mineral].update({

                    "xaxis": xaxis_id,
                    "yaxis": yaxis_id,
                    "xaxis_name": inset_axis_name_x,
                    "yaxis_name": inset_axis_name_y,
                    "x": self.p.capacity_df["Year"].values,
                    "y": []
                })


                # Define inset axes
                self.p.fig.update_layout({
                    xaxis_id: dict(domain=inset_x, anchor=f"y{inset_id}", nticks=3),
                    yaxis_id: dict(domain=inset_y, anchor=f"x{inset_id}", nticks=3)
                })



                # Draw border around inset
                self.p.fig.add_shape(
                    type="rect",
                    xref="paper", yref="paper",
                    x0=inset_x[0], y0=inset_y[0],
                    x1=inset_x[1], y1=inset_y[1],
                    line=dict(color="gray"),
                    fillcolor="white",
                    layer="below",
                )

            return self

        def add_demand_traces(self, demand_map):

            for i, mineral in enumerate(self.p.minerals):
                if mineral not in demand_map:
                    continue
                row, col = (i // 2 + 1, i % 2 + 1)
                y_vals = demand_map[mineral]
                self.p.fig.add_trace(
                    go.Scatter(
                        x=self.p.capacity_df["Year"],
                        y=y_vals,
                        mode="lines+markers",
                        name=mineral,
                        line=dict(color=self.color_map[mineral]),
                        showlegend=False,
                    ),
                    row=row,
                    col=col,
                )

                self.inset_axes[mineral]['y'] = y_vals

            return self



        def update_inset_traces(self):


            for mineral, data in self.inset_axes.items():
                xaxis_id = data['xaxis']
                yaxis_id = data['yaxis']
                demand_x = data['x']
                demand_y = data['y'] / 1e3

                m = (demand_x >= 2025) & (demand_x <= 2026)
                demand_x_zoom = demand_x[m]

                # Increase resolution through linear interpolation
                n = 1000
                X_zoom_interpolated = np.linspace(demand_x_zoom[0], demand_x_zoom[-1], n)
                Y_zoom_interpolated = np.interp(X_zoom_interpolated, demand_x, demand_y)

                # Pick random indices and adjust the axis window
                ix = [500, 510]
                self.p.fig.update_layout({
                    xaxis_id: dict(range=X_zoom_interpolated[ix]),
                    yaxis_id: dict(range=Y_zoom_interpolated[ix])
                })


                # Add inset trace
                self.p.fig.add_trace(
                    go.Scatter(
                        x=demand_x,
                        y=demand_y,
                        mode="lines+markers",
                        name=f"{mineral} demand (zoom)",
                        line=dict(color=self.color_map[mineral]),
                        showlegend=False,
                        xaxis=data['xaxis_name'],
                        yaxis=data['yaxis_name'],
                    )
                )

            return self




        def plot(self):
            return self.p.fig


