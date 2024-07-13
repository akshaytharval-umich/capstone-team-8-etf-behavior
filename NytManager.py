import requests
import json
import pickle
import time
from capstone_team_8_etf_behavior import API_Rules
from datetime import datetime, timedelta

#---------------

class NytManager(): 
    # import of requests
    # f"https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    # from datetime import datetime 
    def __init__(self):
        self.query_count = 0 # This is a count of the number of queries performed, reset on a new calendar date

        # Instances from API_Rules file
        self.call_limit = API_Rules.nyt_total_daily_calls #500
        
        # Keep track of dates
        self.last_date = datetime.now()
        
        # Keep track of time elapsed
        self.bucket_start = datetime.now()
        self.bucket_count = 0
        self.bucket_limit = API_Rules.nyt_per_min #5
        self.wait = API_Rules.nyt_wait_per_call_seconds #12

        # Keep track of pagination
        self.total_pages_in_query = 0
        self.last_completed_page = 0
        self.next_page = 0
        self.current_holding = ""

        # Are Queries allowed flag
        self.permission = False
    
    # Saving & Load Pickle Files pickle files
    def save_progress(self,filepath):
        with open(filepath,'wb') as filepickle:
            pickle.dump(self,filepickle)
    
    @classmethod
    def load_pickle(cls,filepath):
        with open(filepath,'rb') as filepickle:
            save = pickle.load(filepickle)
        return save

    def check_permission(self):
        # A method that checks whether a request should be made
        # Check if the calendar date has changed
        if self.last_date.day != datetime.now().day:
            # set a new last_date
            self.last_date = datetime.now()
            # Additionally, reset the query_count
            self.query_count = 0
            self.bucket_count = 0
            self.bucket_start = datetime.now()
            return True
        elif (self.query_count <= self.call_limit)\
            and (self.bucket_count <= self.bucket_limit):
                # Currently, underneath the limit
            return True
        else:
            # Currently, above the limit
            return False
    
    # A method that receives a query to request
    def submit_query(self,query):
        # First check that there is permission to make a request
        self.permission = self.check_permission()
        if self.permission == True:
            # True, then make request
            # But wait for at least 12 seconds
            time.sleep(self.wait)
            response = requests.get(query)

            # Update the counter
            self.query_count = self.query_count + 1
            self.bucket_count = self.bucket_count + 1

            # Check for bucket timing
            if (datetime.now() - self.bucket_start) > timedelta(minutes=5):
                # longer than 5 minutes, reset
                self.bucket_start = datetime.now()
                self.bucket_count = 0

            # Check if the response was successful
            if response.status_code == 200:
                # With success return the response as a dictionary
                dic = response.json()
                return ('SUCCESS',dic)
            elif response.status_code == 429:
                print("Rate limited by API, terminate process (retry later?)")
                print(response.headers)
                self.permission = False
                return ("LIMIT REACHED",429) # specific flag to save current progress
            else:
                print(f"Unexpected status code {response.status_code}")
                return ("ERROR",response.status_code)
        else:
            # False, then do not make request, return a False
            print("No permission to request currently")
            return ("NOT PERMITTED",False)

