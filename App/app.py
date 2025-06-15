from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from App.Layout import layout
import App.constants as c
from functools import lru_cache


# Define a fixed color mapping for cathode types
nmc_cathodes = ["NMC111", "NMC532", "NMC622", "NMC811"]
lib_cathodes = ['LiFePO4', 'LiCoO2', 'LiCo2O4','LiTiS2','LiMn2O4', 'LiMnO2','LiNiO2','LiNiCoAlO2(0.8:0.15:0.05)']
mineral_colors =  ['#636efa','#EF553B', "#6cd7ba", '#ab63fa']
nmc_colors = dict(zip(nmc_cathodes, mineral_colors))

@lru_cache
def load_data():
    combined = pd.read_parquet("Assets/CombinedMiningData.parquet")
    reserves = pd.read_parquet("Assets/CumulativeReserves.parquet")
    demand_by_cathode = pd.read_parquet("Assets/DemandByCathode.parquet")
    return combined, reserves, demand_by_cathode

combined, reserves, demand_by_cathode = load_data()

def plot_cathodes(reserves_df, demand_df, cathodes, cathode_title, offset=0.1, cathode_colors=None):
    minerals = reserves_df["Primary Mineral"].unique()
    cathodes_plot = make_subplots(rows=2, cols=2, x_title="Year", y_title="Reserves", subplot_titles=minerals.tolist())
    for i, mineral in enumerate(minerals):
        M = reserves_df.loc[(reserves_df["Primary Mineral"] == mineral)]
        S = demand_df.loc[demand_df["Full Element Name"] == mineral, ["Year"] + cathodes]

        # Add the main mineral trace with its own legend group
        cathodes_plot.add_trace(
            go.Scatter(
                x=M["Year"], 
                y=M["Cumulative Reserves"], 
                mode="lines+markers",
                legendgroup=mineral,
                name=mineral,
                marker=dict(
                    size=10,
                    color="black"
                ), 
                showlegend=True,
                legend="legend1"
            ),
            row=i // 2 + 1, 
            col=i % 2 + 1
        )

        # Add cathode traces grouped by cathode type
        for cathode in S[cathodes]:
            cathodes_plot.add_trace(
                go.Scatter(
                    x=S["Year"], 
                    y=S[cathode], 
                    mode="markers",
                    legendgroup=cathode,  # Group by cathode type instead of mineral
                    name=cathode,
                    marker=dict(size=10,color=cathode_colors[cathode] if cathode_colors else None),
                    # Only show in legend for last mineral to avoid duplicates
                    showlegend=(i == 0),
                    legend="legend2",
                ),
                row=i // 2 + 1, 
                col=i % 2 + 1)

        # Add vertical line and annotation
        cathodes_plot.add_vline(x=2024, line_dash="dash", line_color="red")
        cathodes_plot.add_annotation(
            x=2024, 
            text="Current Year",
            showarrow=True,
            arrowhead=2,
            yshift=10,
            row=i // 2 + 1, 
            col=i % 2 + 1
        )


    cathodes_plot.update_yaxes(type='log')
    cathodes_plot.update_layout(title="Cumulative Growth in Reserves Over the Years",height=700,showlegend=True,
                    legend1=dict(title=dict(text="Mineral")),
                    legend2=dict(title=dict(text=cathode_title), y=offset), font=dict(size=20))
    cathodes_plot.update_annotations(font_size=20)
    return cathodes_plot



# Create plots for NMC and LIB cathodes
nmc_cathodes_plot = plot_cathodes(reserves, demand_by_cathode, nmc_cathodes, "NMC Cathodes", cathode_colors=nmc_colors, offset=0.1)
lib_cathodes_plot = plot_cathodes(reserves, demand_by_cathode, lib_cathodes, "LIB Cathodes", cathode_colors=None, offset=-0.1)


sqrt_reserves = np.sqrt(combined["Primary Reserves and Resources"])

reserve_map = px.scatter_geo(combined, lat="Latitude (degrees)", lon="Longitude (degrees)", color="Primary Mineral", 
                    size=sqrt_reserves,
                    size_max=30, hover_data=["Property ID","Primary Reserves and Resources", "Country/Region"],)

reserve_map.update_layout(title="Map of Reserves")


import dash
from dash.dependencies import Input, Output, State
from dash import dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Critical Minerals Assessments"
server = app.server

app.layout = layout

@app.callback(
    Output(c.BODY_ID, 'children'),
    [Input(c.DROPDOWN_ID, 'value')],
)
def update_dropdown(selected_value):
    if selected_value == c.DropDownOptions.NMC.value:
        return dcc.Graph(figure=nmc_cathodes_plot)
    elif selected_value == c.DropDownOptions.LIB.value:
        return dcc.Graph(figure=lib_cathodes_plot)
    elif selected_value == c.DropDownOptions.RESERVES_MAP.value:
        return dcc.Graph(figure=reserve_map)
    else:
        raise dash.exceptions.PreventUpdate()

@app.callback(
    State(c.P_INPUT_ID, 'value'), 
    Input(c.BUTTON_ID, 'n_clicks')
)
def on_submit(porosity, click):
    if click and porosity is not None:
        print(porosity, bool(click))



# Run the app

if __name__ == "__main__":
    server.run(debug=True, port=8090) 


