# For the New York Times the rate limit is 500 requests per day and 5 requests per minute.
# The caller should sleep 12 seconds in between calls to avoid hitting the per minute rate limit.
nyt_per_min = 5
nyt_wait_per_call_seconds = 12
nyt_total_daily_calls = 500