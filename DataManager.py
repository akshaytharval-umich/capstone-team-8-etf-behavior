import pandas as pd
from capstone_team_8_etf_behavior import API_Rules
from datetime import datetime, timedelta
#---------

class DataManager():
    def __init__(self):
        self.data = pd.DataFrame()
        
    def create_data_table(self):
        # For a new creation of the data table
        # First step, create the start date for each range
        start_date_initial = pd.Timestamp('2010-09-06')
        end_date_initial = start_date_initial + timedelta(days=6)
        # Then we need to find the last 2 mondays
        todays_date = datetime.now()
        zero_index_weekday = todays_date.weekday()%7
        # If zero, timedelta will be zero
        last_monday = todays_date - timedelta(zero_index_weekday)
        earlier_monday = last_monday - timedelta(days=7)
        # Then create the ranges
        start_date_range = pd.date_range(start=start_date_initial, end=earlier_monday, freq='W-MON')
        end_date_range = pd.date_range(start=end_date_initial, end=last_monday, freq='W-MON')
        # These two ranges create the index and first column
        self.data = pd.DataFrame(end_date_range,index=start_date_range)
        # Rename from the default 0 to end date
        self.data.columns=['end_date']
        # Next we need to populate with the ten columns
        for name in API_Rules.company_name_top_ten:
            self.data[name] = 0
    
    #@classmethod
    def load_data_table(self,filepath):
        self.data = pd.read_csv(filepath,index_col=0)
    
    def save_data_table(self,filepath):
        self.data.to_csv(filepath,index=True)
    
    
