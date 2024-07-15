# For the New York Times the rate limit is 500 requests per day and 5 requests per minute.
# The caller should sleep 12 seconds in between calls to avoid hitting the per minute rate limit.
nyt_per_min = 5
nyt_wait_per_call_seconds = 13 #technically 12, but hit a bad permission
nyt_total_daily_calls = 500
symbols_top_ten = ['MSFT','AAPL','NVDA','AMZN','META','GOOGL','GOOG','BRK-B','LLY','JPM']
company_name_top_ten = ['Microsoft','Apple','NVIDIA','Amazon','Meta','Alphabet (Class A)','Alphabet (Class C)',
                        'Berkshire Hathaway','Eli Lilly','JPMorgan Chase']