import time
from datetime import datetime, timedelta
import API_Rules # To get API numbers
import os

class NytQueryBuilder():
    def build_query(self,holding=None,begin_date=None,end_date=None,page=1):

        nyt_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
        # If no holding specified, then nothing to build
        if holding not in API_Rules.symbols_top_ten:
            return None
        else:
            nyt_url = nyt_url + f"q={holding}"
        
        # Add the api key from the environment
        nyt_url = nyt_url + f"&api-key={os.environ['NYTIMES_KEY']}"
         
        # Next, add the date it should begin at
        if begin_date is not None:
            nyt_url = nyt_url + f"&begin_date={begin_date.strftime("%Y%m%d")}"
        
        # Also add an end date if provided
        if end_date is not None:
            nyt_url = nyt_url + f"&end_date={end_date.strftime("%Y%m%d")}"
        
        # Next, keep things as the business desk for now
        nyt_url = nyt_url + f'&fq=news_desk:("Business")'

        # if a page is given
        nyt_url = nyt_url + f"&page={page}"

        #sort
        nyt_url = nyt_url + f"&sort='oldest'"

        return nyt_url