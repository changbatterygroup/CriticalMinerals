
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

from plotly.subplots import make_subplots
import plotly.graph_objects as go


minerals = ["Manganese", "Lithium", "Cobalt", "Nickel", "Lanthanides"]
data_directory = "./data" # Set this to your own directory



combined = None

mining_path = os.path.join(data_directory, "SPGlobal_MetalsAndMiningProperties-Combined-Dec-2024.xlsx")
for i, mineral in enumerate(minerals):
    data = pd.read_excel(mining_path, sheet_name = mineral)
    print(f"Read {mineral}")

    # data.dropna(subset="Primary Reserves and Resources", inplace = True)
    data["Reserves & Resources As Of Date"] = pd.to_datetime(data["Reserves & Resources As Of Date"])
    data["Primary Mineral"] = mineral
    data["Year"] = data["Reserves & Resources As Of Date"].dt.year


    if i == 0:
        combined = data
        continue

    combined = pd.concat([combined, data], ignore_index=True)

combined = combined.sort_values(by = "Year").query("`Activity Status` == 'Active'")
combined["Property ID"] = combined["Property ID"].astype(int)


locations = pd.read_excel("data/MiningPropertyLocations.xlsx")
coords = locations[["KeyMineProject","Latitude (degrees)", "Longitude (degrees)"]]

combined = combined.merge(coords, left_on = "Property ID", right_on="KeyMineProject" ,how = "inner")
combined.drop("KeyMineProject", axis=1, inplace=True, errors="ignore")



start_year = 2010
combined = combined[combined["Year"] >= start_year]




D = combined[["Year","Primary Mineral", "Primary Reserves and Resources"]]

D = D.groupby(["Year","Primary Mineral"], as_index=False).agg("sum")


# Generate a complete set of Year-Mineral combinations
all_years = D["Year"].unique()
all_minerals = D["Primary Mineral"].unique()
complete_index = pd.MultiIndex.from_product([all_years, all_minerals], names=["Year", "Primary Mineral"])

# Reindex the DataFrame to include all combinations, filling missing values with 0
D = D.set_index(["Year", "Primary Mineral"]).reindex(complete_index, fill_value=0).reset_index()
D["Cumulative Reserves"] = D.groupby(["Primary Mineral"], as_index=False)["Primary Reserves and Resources"].agg("cumsum")
D = D[D["Primary Reserves and Resources"] > 0]





# Extend to Future Years
for yr in range(2025, 2030+1):
    latest = D[D["Year"]==2024]
    latest.loc[:,"Year"] = yr
    D = pd.concat([D, latest], axis=0)



demand_by_cathode = pd.read_excel(os.path.join(data_directory, "Capacity.xlsx"), sheet_name="Demand by Cathode")
demand_by_cathode = demand_by_cathode.loc[demand_by_cathode.Element != "O"]
demand_by_cathode = demand_by_cathode[~((demand_by_cathode.Element == "Li") & (demand_by_cathode["+"] == False))]
demand_by_cathode.drop(["Element", "+"], axis=1, inplace=True)
demand_by_cathode = demand_by_cathode.iloc[:,:-5] # Last 5 are redundant
demand_l = demand_by_cathode.melt(id_vars=["Year", "Full Element Name"], var_name="Cathode", value_name="demand").dropna()


non_lanthanides_df = combined[combined["Primary Mineral"] != "Lanthanides"]
non_lanthanides_reserves_c = D[D["Primary Mineral"] != "Lanthanides"]

# Define a fixed color mapping for cathode types
nmc_cathodes = ["NMC111", "NMC532", "NMC622", "NMC811"]
lib_cathodes = ['LiFePO4', 'LiCoO2', 'LiCo2O4','LiTiS2','LiMn2O4', 'LiMnO2','LiNiO2','LiNiCoAlO2(0.8:0.15:0.05)']
mineral_colors =  ['#636efa','#EF553B', "#6cd7ba", '#ab63fa']
nmc_colors = dict(zip(nmc_cathodes, mineral_colors))







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





nmc_cathodes_plot = plot_cathodes(non_lanthanides_reserves_c, demand_by_cathode, nmc_cathodes, "NMC Cathodes", cathode_colors=nmc_colors, offset=0.1)
lib_cathodes_plot = plot_cathodes(non_lanthanides_reserves_c, demand_by_cathode, lib_cathodes, "LIB Cathodes", cathode_colors=None, offset=-0.1)






sqrt_reserves = np.sqrt(non_lanthanides_df["Primary Reserves and Resources"])

reserve_map = px.scatter_geo(non_lanthanides_df, lat="Latitude (degrees)", lon="Longitude (degrees)", color="Primary Mineral", 
                    size=sqrt_reserves,
                    size_max=30, hover_data=["Property ID","Primary Reserves and Resources", "Country/Region"],)

reserve_map.update_layout(title="Map of Reserves")


import dash
from dash import dcc, html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Critical Minerals Assessments"

app.layout = html.Div([
    html.H1("Critical Minerals Assessments"),
    html.P("This is a placeholder description"),
    html.Label("Select a plot to view:"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'NMC Cathodes', 'value': 'nmc'},
            {'label': 'LIB Cathodes', 'value': 'lib'},
            {'label': 'Reserve Map',  'value': 'reserve_map'}
        ],
        value='nmc',
        clearable=False
    ),
    html.Div(id='placeholder')

])

@app.callback(
    dash.dependencies.Output('placeholder', 'children'),
    [dash.dependencies.Input('dropdown', 'value')],
)
def update_dropdown(selected_value):


    if selected_value == 'nmc':
        return dcc.Graph(figure=nmc_cathodes_plot)
    elif selected_value == 'lib':
        return dcc.Graph(figure=lib_cathodes_plot)
    elif selected_value == 'reserve_map':
        return dcc.Graph(figure=reserve_map)
    else:
        raise dash.exceptions.PreventUpdate()



# Run the app

if __name__ == "__main__":
    app.run(debug=True, port=8090, jupyter_mode="external") 


