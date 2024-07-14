import os
from datetime import datetime
from capstone_team_8_etf_behavior.NytManager import NytManager
from capstone_team_8_etf_behavior.DataManager import DataManager
from capstone_team_8_etf_behavior.NytQueryBuilder import NytQueryBuilder

def scrape():
    # First does a handler exist?
    api_manager_path = "capstone_team_8_etf_behavior/api_manager.pkl"
    if os.path.exists(api_manager_path):
        # Use class method
        api_manager = NytManager.load_pickle(api_manager_path)
        print("API Manager exists, loading in")
    else:
        # Doesn't exist, make new file
        api_manager = NytManager()
        api_manager.save_progress(api_manager_path)
        print("Created new API manager")

    # Next instance does the tracker exist?
    data_manager_path = "capstone_team_8_etf_behavior/data_manager.csv"
    if os.path.exists(data_manager_path):
        # Use class method
        data_manager = DataManager()
        data_manager.load_data_table(data_manager_path)
        # Will need to build method to udpate additional weeks
        print("Data Manager exists, loading in")
    else:
        # Doesn't exist, make new file
        data_manager = DataManager()
        # Create a new table
        data_manager.create_data_table()
        data_manager.save_data_table(data_manager_path)
        print("Created new data manager")
    
    #