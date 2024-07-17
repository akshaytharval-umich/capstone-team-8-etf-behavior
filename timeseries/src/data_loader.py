import pandas as pd

def load_data(file_path):
    """Load the stock price data from a CSV file."""
    return pd.read_csv(file_path)
