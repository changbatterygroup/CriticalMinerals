#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os


# In[ ]:


minerals = ["Manganese", "Lithium", "Cobalt", "Nickel", "Lanthanides"]
data_directory = "./data" # Set this to your own directory


# In[4]:


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


# In[5]:


locations = pd.read_excel("data/MiningPropertyLocations.xlsx")
coords = locations[["KeyMineProject","Latitude (degrees)", "Longitude (degrees)"]]

combined = combined.merge(coords, left_on = "Property ID", right_on="KeyMineProject" ,how = "inner")
combined.drop("KeyMineProject", axis=1, inplace=True, errors="ignore")


# In[6]:


start_year = 2010
combined = combined[combined["Year"] >= start_year]


# In[7]:


from io import StringIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error


d = """
Year,Capacity
2010,14
2011,28
2012,38
2013,56
2014,75
2015,85
2016,111
2017,198
2018,293.7
2022,1570
2025,3970
2030,6790
"""

df = pd.read_csv(StringIO(d))
df["log_capacity"] = np.log(df["Capacity"])


# In[8]:


errors = []
models = []
transforms = []
r = np.arange(1,20)
for d in r:
    poly = PolynomialFeatures(degree=d, include_bias=True)
    transforms.append(poly)
    X = poly.fit_transform(df[["Year"]], df["log_capacity"])
    reg = LinearRegression()
    reg.fit(X, df[["log_capacity"]].values)
    models.append(reg)
    rmse = root_mean_squared_error(df["log_capacity"],reg.predict(X))
    errors.append(rmse)


errors = np.array(errors)
differences = np.abs(np.diff(errors))
threshold = 0.001
best_index = np.argmax(differences[differences > 0] < threshold)
best_poly = transforms[best_index]
best_model = models[best_index]
print(f"Best degree: {best_index + 1} with RMSE {errors[best_index]}")

plt.plot(errors, marker="o")
plt.xticks(r - 1,labels=r)
plt.xlabel("Polynomial Degree")
plt.ylabel("RMSE")
plt.show()

print(best_model.coef_, best_model.intercept_)


# In[9]:


year_range = np.arange(df["Year"].min(), df["Year"].max())

p2 = pd.DataFrame(year_range[~np.isin(year_range, df["Year"])], columns=["Year"])
p2["log_capacity"] = best_model.predict(best_poly.transform(p2[["Year"]]))
p2["Capacity"] = np.exp(p2[["log_capacity"]])
df_full = pd.concat([df, p2], axis=0).sort_values("Year").reset_index(drop=True)
# df_full.to_excel(os.path.join(data_directory, "Capacity.xlsx"),  sheet_name="Projected Capacity", index=False)

ax = df_full.plot(x="Year", y="Capacity", marker="o")
ax.set_ylabel("Capacity (GWh)")
ax.set_xticks(df_full["Year"], df_full["Year"])
ax.tick_params(axis='x', rotation=-45)
for label in ax.get_xticklabels():
    label.set_ha('left')

plt.legend().remove()
plt.title("Projected Battery Production Capacity")
plt.show()


# In[10]:


combined["Primary Mineral"].unique()


# In[11]:


reserves_over_time = combined \
        .groupby(["Reserves & Resources As Of Date", "Primary Mineral"], as_index = False)["Primary Reserves and Resources"] \
        .agg("sum")


fig = px.line(reserves_over_time, x="Reserves & Resources As Of Date", facet_col = "Primary Mineral",
        y="Primary Reserves and Resources", log_y = True, facet_col_wrap=2, facet_row_spacing=0.2)

fig.update_xaxes(title_text="Date")
fig.update_layout(title = "Total Reserves Over the Years")
fig.update_yaxes(title_text=None)
fig.show()


# In[127]:


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


# In[129]:


# Extend to Future Years
for yr in range(2025, 2030+1):
    latest = D[D["Year"]==2024]
    latest.loc[:,"Year"] = yr

    D = pd.concat([D, latest], axis=0)




# In[74]:


demand_by_cathode = pd.read_excel(os.path.join(data_directory, "Capacity.xlsx"), sheet_name="Demand by Cathode")
demand_by_cathode = demand_by_cathode.loc[demand_by_cathode.Element != "O"]

demand_by_cathode = demand_by_cathode[~((demand_by_cathode.Element == "Li") & (demand_by_cathode["+"] == False))]
demand_by_cathode.drop(["Element", "+"], axis=1, inplace=True)

demand_by_cathode = demand_by_cathode.iloc[:,:-5] # Last 5 are redundant
demand_by_cathode.head()


# In[148]:


demand_l = demand_by_cathode.melt(id_vars=["Year", "Full Element Name"], var_name="Cathode", value_name="demand").dropna()


# In[167]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go


non_lanthanides_df = combined[combined["Primary Mineral"] != "Lanthanides"]
non_lanthanides_reserves_c = D[D["Primary Mineral"] != "Lanthanides"]

# Define a fixed color mapping for cathode types
nmc_cathodes = ["NMC111", "NMC532", "NMC622", "NMC811"]
lib_cathodes = ['LiFePO4', 'LiCoO2', 'LiCo2O4','LiTiS2','LiMn2O4', 'LiMnO2','LiNiO2','LiNiCoAlO2(0.8:0.15:0.05)']
mineral_colors =  ['#636efa','#EF553B', "#6cd7ba", '#ab63fa']
nmc_colors = dict(zip(nmc_cathodes, mineral_colors))




# In[168]:


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


# In[171]:


nmc_cathodes_plot = plot_cathodes(non_lanthanides_reserves_c, demand_by_cathode, nmc_cathodes, "NMC Cathodes", cathode_colors=nmc_colors, offset=0.1)
lib_cathodes_plot = plot_cathodes(non_lanthanides_reserves_c, demand_by_cathode, lib_cathodes, "LIB Cathodes", cathode_colors=None, offset=-0.1)

nmc_cathodes_plot.show()
lib_cathodes_plot.show()


# In[172]:


sqrt_reserves = np.sqrt(non_lanthanides_df["Primary Reserves and Resources"])

reserve_map = px.scatter_geo(non_lanthanides_df, lat="Latitude (degrees)", lon="Longitude (degrees)", color="Primary Mineral", 
                    size=sqrt_reserves,
                    size_max=30, hover_data=["Property ID","Primary Reserves and Resources", "Country/Region"],)

reserve_map.update_layout(title="Map of Reserves")


# In[22]:


lanthanides_df = combined[combined["Primary Mineral"] == "Lanthanides"]

sqrt_reserves = np.sqrt(lanthanides_df["Primary Reserves and Resources"])

fig = px.scatter_geo(lanthanides_df, lat="Latitude (degrees)", lon="Longitude (degrees)",
                    size=sqrt_reserves,
                    size_max=20, hover_data=["Property ID","Primary Reserves and Resources", "Country/Region"],)

fig.update_layout(title="Map of Lanthanides Reserves",margin=dict(l=5, r=5, t=30, b=30))
fig.show()


# In[ ]:


# C = combined.copy()
# usca = C[C["Primary Mineral"].isin(["Cobalt", "Nickel", "Manganese"]) & 
#          C["Country/Region"].isin(["USA", "Canada"])]
# usca


# In[49]:


# import networkx as nx
# from geopy.distance import geodesic
# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# from sklearn.cluster import DBSCAN
# from sklearn.preprocessing import LabelEncoder

# def build(df, required_metals = {"Cobalt", "Nickel", "Manganese"} ,max_distance_per_cluster=7000):  # km

#     simplified_df = df.rename(columns={'Latitude (degrees)': 'Lat', 
#                        'Longitude (degrees)': 'Lon',
#                         'Primary Reserves and Resources': 'Reserves',
#                         'Property ID': 'ID',
#                         'Property': 'Name'})


#     simplified_df['Normalized_Reserves'] = simplified_df['Reserves'] / simplified_df['Reserves'].max()

#     coords = simplified_df[['Lat', 'Lon']]
#     clustering = DBSCAN(eps=max_distance_per_cluster/1000, min_samples=4).fit(coords)
#     simplified_df['Cluster'] = clustering.labels_

#     fig = go.Figure()



#     def check_coverage(sites):
#         found = set()
#         for s in sites:
#             for metal in required_metals:
#                 if metal.lower() in s['Primary Mineral'].lower():
#                     found.add(metal)
#         return required_metals.issubset(found)

#     for cluster in simplified_df['Cluster'].unique():
#         if cluster == -1:
#             continue

#         cluster_data = simplified_df[simplified_df['Cluster'] == cluster].copy()
#         if cluster_data.empty:
#             continue

#         fig.add_trace(go.Scattergeo(
#             lon=cluster_data['Lon'],
#             lat=cluster_data['Lat'],
#             customdata=cluster_data[['Reserves', 'Name', 'Commodity(s)', "Primary Mineral"]],
#             mode='markers+text',
#             hovertemplate="<b>%{customdata[1]}</b><br>" +
#                           "Latitude: %{lat}<br>" +
#                           "Longitude: %{lon}<br>" +
#                           "Commodities: %{customdata[2]}<br>" +
#                           "Primary Commodity: %{customdata[3]}<br>" +
#                           "Reserves: %{customdata[0]:,.0f} tonnes",
#             textposition="bottom center",
#             marker=dict(size=8, symbol='circle'),
#             name=f'Cluster {cluster}'
#         ))

#         # Greedy selection algorithm with metal constraint
#         mines = cluster_data.to_dict(orient='records')
#         start = max(mines, key=lambda x: x['Reserves'])

#         visited = [start]
#         unvisited = [m for m in mines if m['ID'] != start['ID']]
#         total_distance = 0

#         while unvisited:
#             best_mine = None
#             best_score = float('-inf')
#             best_distance = None

#             for candidate in unvisited:
#                 dist = geodesic(
#                     (visited[-1]['Lat'], visited[-1]['Lon']),
#                     (candidate['Lat'], candidate['Lon'])
#                 ).km
#                 if dist == 0:
#                     continue
#                 score =  candidate['Reserves'] / dist
#                 if score > best_score:
#                     best_score = score
#                     best_mine = candidate
#                     best_distance = dist

#             if best_distance and total_distance + best_distance <= max_distance_per_cluster:
#                 total_distance += best_distance
#                 visited.append(best_mine)
#                 unvisited = [u for u in unvisited if u['ID'] != best_mine['ID']]
#             else:
#                 break

#             # # If constraint satisfied, we can optionally stop early
#             # if check_coverage(visited):
#             #     break

#         # Try adding backup mines just to fulfill constraints
#         if not check_coverage(visited):
#             for backup in sorted(unvisited, key=lambda x: -x['Reserves']):
#                 dist = geodesic(
#                     (visited[-1]['Lat'], visited[-1]['Lon']),
#                     (backup['Lat'], backup['Lon'])
#                 ).km
#                 if total_distance + dist > max_distance_per_cluster:
#                     continue
#                 visited.append(backup)
#                 total_distance += dist
#                 if check_coverage(visited):
#                     break

#         # Draw path
#         for i in range(len(visited) - 1):
#             node1 = visited[i]
#             node2 = visited[i + 1]
#             fig.add_trace(go.Scattergeo(
#                 lon=[node1['Lon'], node2['Lon']],
#                 lat=[node1['Lat'], node2['Lat']],
#                 mode='lines',
#                 line=dict(width=2, color='gray'),
#                 showlegend=False
#             ))

#     fig.update_layout(
#         title="Constraint-Aware Resource Route: Covering Key Metals",
#         margin=dict(l=5, r=5, t=30, b=30),
#         geo=dict(
#             scope='world',
#             showland=True,
#             landcolor='lightgray',
#             countrycolor='white',
#             lonaxis=dict(range=[simplified_df["Lon"].min() - 10, simplified_df["Lon"].max() + 10]),
#             lataxis=dict(range=[simplified_df["Lat"].min() - 10, simplified_df["Lat"].max() + 10])
#         ),
#         template="plotly_white"
#     )

#     fig.show()


# In[ ]:


# build(C[C["Primary Mineral"] != "Lanthanides"], max_distance_per_cluster=7000)


# In[50]:


# import networkx as nx
# from geopy.distance import geodesic
# import numpy as np

# G = nx.Graph()

# # Add nodes
# for _, row in usca.iterrows():
#     G.add_node(row["Property ID"], primary_mineral=row["Primary Mineral"], name=row["Property"], 
#                pos=(row["Latitude (degrees)"], row["Longitude (degrees)"]), 
#                reserves=row["Primary Reserves and Resources"])

# # Add weighted edges
# for i, row1 in usca.iterrows():
#     for j, row2 in usca.iterrows():
#         if i < j:  # Avoid duplicate edges
#             dist = geodesic((row1["Latitude (degrees)"], row1["Longitude (degrees)"]), 
#                             (row2["Latitude (degrees)"], row2["Longitude (degrees)"])).km
#             weight = dist / np.log(row1["Primary Reserves and Resources"])

#             G.add_edge(row1["Property ID"], row2["Property ID"], weight=weight)

# # Compute Minimum Spanning Tree (MST)
# mst = nx.minimum_spanning_tree(G, weight='weight')



# In[ ]:


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
app.run(debug=True, port=8050, jupyter_mode="external", use_reloader=True) 


# In[ ]:




