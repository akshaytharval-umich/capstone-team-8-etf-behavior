import os
import pandas as pd
from datetime import datetime
from capstone_team_8_etf_behavior.NytManager import NytManager
from capstone_team_8_etf_behavior.DataManager import DataManager
from capstone_team_8_etf_behavior.NytQueryBuilder import NytQueryBuilder

def scrape(holding=None):
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
    
    # This is where we need to loop as long
    query_response = True
    lst = []

    while query_response != False:
        
        # Next determine the row in the data_manager.csv to query
        row_label = data_manager.data[data_manager.data[holding]!=-1].index[0]
        print(f"Row label {row_label}")
        
        # With the row number determine the query elements
        begin = datetime.strptime(row_label, '%Y-%m-%d')
        end_datetime = data_manager.data.at[row_label,'end_date']
        end = datetime.strptime(end_datetime, '%Y-%m-%d')
        pagination = data_manager.data.at[row_label,holding]
        print(f"{holding} : {pagination} : {begin} : {end}")
        builder = NytQueryBuilder()
        query = builder.build_query(holding=holding,begin_date=begin,end_date=end,page=pagination)
        print(query)
        
        # With the query, what do we get back?
        result = api_manager.submit_query(query)
        # If the query is a success
        if result[0] == "SUCCESS" and result[1]['status'] == 'OK':
            # Returned real result, the second argument of the result is a dictionary with the response key
            response = result[1]['response']
            # With a dictionary of docs and meta, are hits less than 10
            difference = int(response['meta']['hits'] - response['meta']['offset'])
            # difference holds the number of remaining results
            if difference > 10:
                print("Requires Pagination")
                # Then more queries required, return offset increased by 10
                update = pagination + 1 # this advances the results by 10
            else:
                # This is the remaining hits, return -1
                print("Complete Week")
                update = -1
            data_manager.data.at[row_label,holding] = update # updates the data_manager
            print("Update Value")
            print(data_manager.data.at[row_label,holding]) 
            lst.extend(response['docs'])
            query_response = True
            
        else:
            # then if it didn't succeed we need to stop and save
            query_response = False

    # Create a pandas dataframe from the lst
    df = pd.DataFrame(lst)
    df['holding'] = holding

    # Does an existing articles.csv exist?
    articles_path = "capstone_team_8_etf_behavior/articles.csv"
    if os.path.exists(articles_path):
        print("previous csv exists, combining")
        loaded_frame = pd.read_csv(articles_path)
        df = pd.concat([loaded_frame,df],encoding='utf-8',ignore_index=True)
    df.to_csv(articles_path,encoding='utf-8')
    print("articles.csv exported")

    #export over the existing csv for the data_manager
    data_manager.save_data_table(data_manager_path)
    print("data_manager.csv exported")

    # Save the API Manager
    api_manager.save_progress(api_manager_path)
    print("API Manager has been saved")
    print('Scraping ended')
        