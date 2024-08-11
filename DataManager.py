
import pandas as pd
import API_Rules
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
        end_date_range = pd.date_range(start=end_date_initial, end=last_monday, freq='W-SUN')
        # These two ranges create the index and first column
        self.data = pd.DataFrame(end_date_range,index=start_date_range)
        # Rename from the default 0 to end date
        self.data.columns=['end_date']
        # Next we need to populate with the ten columns
        for name in API_Rules.company_name_top_ten:
            self.data[name] = 0
            self.data[name] = self.data[name].astype(int) # to ensure integer for pagination
    
    def update_data_table(self):
        # this function takes a dataframe and adds to the last complete week
        # need to compare the last date of the data table
        start_date_in_file = pd.Timestamp(self.data.index[-1]) + timedelta(days=7)
        end_date_in_file = pd.Timestamp(self.data['end_date'].iloc[-1]) + timedelta(days=7)
        # find the ending of both ranges
        todays_date = datetime.now()
        zero_index_weekday = todays_date.weekday()%7
        last_monday = todays_date - timedelta(zero_index_weekday)
        earlier_monday = last_monday - timedelta(days=7)
        # create the ranges
        start_date_range = pd.date_range(start=start_date_in_file, end=earlier_monday, freq='W-MON')
        end_date_range = pd.date_range(start=end_date_in_file, end=last_monday, freq='W-SUN')
        new_df = pd.DataFrame(end_date_range,index=start_date_range)
        new_df.columns=['end_date']
        # Add the same holdings as the initial creation
        for name in API_Rules.company_name_top_ten:
            new_df[name] = 0
            new_df[name] = new_df[name].astype(int) # to ensure integer for pagination
        self.data = pd.concat([self.data,new_df],ignore_index=False)

    #@classmethod
    def load_data_table(self,filepath):
        self.data = pd.read_csv(filepath,encoding='utf-8',index_col=0)
    
    def save_data_table(self,filepath):
        self.data.to_csv(filepath,encoding='utf-8',index=True)
    
    
