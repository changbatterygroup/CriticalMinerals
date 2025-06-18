from .ReservesPlotter import ReservesPlotter
from Backend.DataLoader import DataLoader
from .DemandPlotter import DemandPlotter


# Define a fixed color mapping for cathode types
# nmc_cathodes = ["NMC111", "NMC532", "NMC622", "NMC811"]
# lib_cathodes = ['LiFePO4', 'LiCoO2', 'LiCo2O4','LiTiS2','LiMn2O4', 'LiMnO2','LiNiO2','LiNiCoAlO2(0.8:0.15:0.05)']
# mineral_colors =  ['#636efa','#EF553B', "#6cd7ba", '#ab63fa']
# nmc_colors = dict(zip(nmc_cathodes, mineral_colors))

reserves = DataLoader.get('cumulative_reserves')
demand_by_cathode =  DataLoader.get('demand_by_cathode')
capacity = DataLoader.get('capacity')
