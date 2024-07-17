import yfinance as yf
import pandas as pd

def get_voo_historical_data():
    """
    Retrieves historical data for the ETF with the ticker symbol 'VOO' and saves it to a CSV file.
    """
    tickerSymbol = '^GSPC'
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start='2000-1-1', end='2011-1-1')
    tickerDf.to_csv('sp_historical_data.csv')

# Call the function to retrieve and save the data
get_voo_historical_data()
