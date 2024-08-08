import yfinance as yf
import pandas as pd

def get_voo_historical_data():
    """
    Retrieves historical data for the ETF with the ticker symbol 'VOO' and saves it to a CSV file.
    """
    tickerSymbol = 'VOO'
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start='2000-1-1', end='2024-12-31')
    tickerDf.to_csv('voo_historical_data.csv')

# Call the function to retrieve and save the data
get_voo_historical_data()
