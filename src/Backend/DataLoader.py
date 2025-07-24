import pandas as pd
from functools import lru_cache
from pathlib import Path

class DataLoader:
    
    ASSET_PATH = Path("Assets")
    
    @staticmethod
    @lru_cache(maxsize=1)
    def _load_all_data():
        """Load all data files once and cache them"""
        data_files = {
            'combined': 'CombinedMiningData.parquet',
            'cumulative_reserves': 'CumulativeReserves.parquet',
            'demand_by_cathode': 'DemandByCathode.parquet',
            'capacity': 'Capacity.parquet'
        }
        
        loaded_data = {}
        for key, filename in data_files.items():
            filepath = DataLoader.ASSET_PATH / filename
            try:
                loaded_data[key] = pd.read_parquet(filepath)
            except FileNotFoundError:
                print(f"Warning: Could not load {filepath}")
                loaded_data[key] = pd.DataFrame()  # Empty dataframe as fallback
        
        return loaded_data
    
    @staticmethod
    def get(key):
        """Get specific dataset by key"""
        return DataLoader._load_all_data()[key]
    
    @staticmethod
    def get_all():
        """Get all datasets"""
        return DataLoader._load_all_data()
    

    
    