import requests
import json
import re
import random
import pickle
import pandas as pd
import time
import API_Rules # To get API numbers
from datetime import datetime, timedelta

#set a random seed for testing
random.seed(42)

#---------------
class NytManager(self,API_Rules.nyt_total_daily_calls):
    # First define initial settings upon creation
    def __init__(self):
        self.query_count = 0 # This is a count of the number of requests performed, reset on a new calendar date
        self.rate_limit = API_Rules.nyt_total_daily_calls #limit in a calendar day
        self.wait_sec = 
        self.


class ApiHandler(): 
    # import of requests
    # f"https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    # from datetime import datetime 
    def __init__(self):
        self.query_count = 0 # This is a count of the number of queries performed, reset on a new calendar date
        self.rate_limit = API_Rules.nyt_total_daily_calls #100,000
        self.last_date = datetime.now()
        self.permission = True
        self.start_time = datetime.now()
        self.deepnote_active_limit = 23.5

    def check_permission(self):
        # A method that checks whether a request should be made
        # Check if the calendar date has changed
        if self.last_date.day != datetime.now().day:
            # set a new last_date
            self.last_date = datetime.now()
            # Additionally, reset the query_count
            self.query_count = 0
            return True
        elif self.query_count <= self.rate_limit:
            # Currently, underneath the limit
            return True
        else:
            # Currently, above the limit
            return False
    
    # A method that receives a query to request
    def submit_query(self,query):
        # First check that there is permission to make a request
        self.permission = self.check_permission()
        # Check if 23.5 hours has passed
        elapsed_time = datetime.now() - self.start_time
        elapsed_hours = elapsed_time.total_seconds()/3600
        if elapsed_hours >= self.deepnote_active_limit:
            print("MAX 23.5 HOURS REACHED")
            return ("LIMIT REACHED",429)
        if self.permission == True:
            # True, then make request
            # But wait for at least 1 second
            time.sleep(5)
            response = requests.get(query)
            # Update the counter
            self.query_count = self.query_count + 1
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