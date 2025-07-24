from Backend.Model import DemandCalculator
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from core.configs.cathode_config import CATHODE_SPECS
from core.schema import DemandParams

lfp_wrapper = DemandCalculator.from_config("LFP")

def plot_reserves(reserve_df):
    minerals = reserve_df["Primary Mineral"].unique().tolist()
    fig = make_subplots( rows=2, cols=2, x_title="Year",  y_title="Reserves", subplot_titles=minerals)
    fig.update_yaxes(type="log")
    fig.update_annotations(font_size=20)
    fig.update_layout(
        title="Cumulative Growth in Reserves vs Demand Over the Years",
        height=700,
        showlegend=True,
        legend1=dict(title=dict(text="Mineral")),
    )

    minerals_used, subplot_domains = add_reserve_traces(fig, reserve_df)
    return fig, minerals_used, subplot_domains


def add_current_year_marker(fig, year=2024, row=None, col=None):
    fig.add_vline(x=year, line_dash="dash", line_color="red", row=row, col=col)
    fig.add_annotation(
        x=year,
        text="Current Year",
        showarrow=True,
        arrowhead=2,
        ax=-30,
        yshift=-50,
        row=row,
        col=col,
    )


def add_reserve_traces(fig, data):
    minerals = data["Primary Mineral"].unique()
    subplot_domains = {}

    for i, mineral in enumerate(minerals):
        mineral_data = data[data["Primary Mineral"] == mineral]
        row, col = i // 2 + 1, i % 2 + 1

        fig.add_trace(
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

        add_current_year_marker(fig, row=row, col=col)

        # Save subplot domain for inset
        subplot_domains[(row, col)] = {
            "x": fig.layout[f"xaxis{row * 2 + col - 2}"].domain,
            "y": fig.layout[f"yaxis{row * 2 + col - 2}"].domain,
        }

    return minerals, subplot_domains


def add_inset_plot(fig, capacity_df, y_vals, mineral, row, col, subplot_domains, color):
    # Prepare data for inset (last few years)
    r = slice(-6, -4, 1)
    demand_x = capacity_df.index[r]
    demand_y = y_vals[r] / 1e3  # scale for better display

    # Fit a small linear trend
    w = np.polyfit(np.array(demand_x), np.array(demand_y), 1)[::-1]
    x_r = np.array([2025.4, 2025.7])
    x_r_b = np.vstack([np.ones_like(x_r), x_r])
    y_r = x_r_b.T @ w

    # Find y-range
    k = 5
    y_min = min(y_r[0] + k, y_r[1] - k)
    y_max = max(y_r[0] + k, y_r[1] - k)

    # Get subplot domain
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

    # Define inset axes
    fig.update_layout({
        xaxis_id: dict(domain=inset_x, anchor=f"y{inset_id}", range=[2025.5, 2025.6], nticks=3),
        yaxis_id: dict(domain=inset_y, anchor=f"x{inset_id}", range=[y_min, y_max])
    })

    # Add inset trace
    fig.add_trace(
        go.Scatter(
            x=demand_x,
            y=demand_y,
            mode="lines+markers",
            name=f"{mineral} demand (zoom)",
            line=dict(color=color),
            showlegend=False,
            xaxis=inset_axis_name_x,
            yaxis=inset_axis_name_y,
        )
    )

    # Draw border around inset
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=inset_x[0], y0=inset_y[0],
        x1=inset_x[1], y1=inset_y[1],
        line=dict(color="gray"),
        fillcolor="white",
        layer="below",
    )


def add_demand_traces(fig, capacity_df, minerals, subplot_domains, category ,cathode, inputs: DemandParams):

    c2_wrapper = DemandCalculator.from_config(cathode)
    capacity_df = capacity_df.set_index("Year")

    needed_nmc = capacity_df["Capacity"] * capacity_df[CATHODE_SPECS[cathode]['category']]
    needed_lfp = capacity_df["Capacity"] * capacity_df[CATHODE_SPECS['LFP']['category']]
    if category in capacity_df.columns:
        needed_nmc *= capacity_df[category]
        needed_lfp *= capacity_df[category]



    t = np.linspace(0, 3600, 100)
    lfp_demand = lfp_wrapper.run(needed_lfp, t, inputs.porosity, inputs.radius, inputs.thickness)
    c2_demand = c2_wrapper.run(needed_nmc, t, inputs.porosity, inputs.radius, inputs.thickness)

    total = lfp_demand
    if cathode != "LFP":
        total += c2_demand

    total_Li, Co_mass, Mn_mass, Ni_mass = total

    mineral_data_map = {
        "Cobalt": Co_mass,
        "Lithium": total_Li,
        "Nickel": Ni_mass,
        "Manganese": Mn_mass,
    }

    color_map = {
        "Cobalt": "darkorange",
        "Lithium": "royalblue",
        "Nickel": "purple",
        "Manganese": "yellowgreen",
    }

    for i, mineral in enumerate(minerals):
        if mineral not in mineral_data_map:
            continue
        row, col = (i // 2 + 1, i % 2 + 1)
        y_vals = mineral_data_map[mineral]
        fig.add_trace(
            go.Scatter(
                x=capacity_df.index,
                y=y_vals,
                mode="lines+markers",
                name=mineral,
                line=dict(color=color_map[mineral]),
                showlegend=False,
            ),
            row=row,
            col=col,
        )

        # Find corresponding reserve trace
        reserve_trace = next((t for t in fig.data if t.name == mineral and t.marker.color == "black"), None)
        if reserve_trace:
            add_inset_plot(fig, capacity_df, y_vals, mineral, row, col, subplot_domains, color_map[mineral])

