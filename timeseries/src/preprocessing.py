import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_data(data):
    """Normalize the 'Close' prices in the data."""
    close_prices = data['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)
    return scaled_data, scaler

def split_data(scaled_data, train_ratio, val_ratio):
    """
    Split the data into training, validation, and testing sets.
    
    Parameters:
    scaled_data (numpy array): The scaled dataset.
    train_ratio (float): The proportion of data to be used for training. Default is 0.7.
    val_ratio (float): The proportion of data to be used for validation. Default is 0.15.
    
    Returns:
    train_data, val_data, test_data: The split datasets.
    """
    train_size = int(len(scaled_data) * train_ratio)
    val_size = int(len(scaled_data) * val_ratio)
    
    train_data = scaled_data[:train_size]
    val_data = scaled_data[train_size:train_size + val_size]
    test_data = scaled_data[train_size + val_size:]
    
    return train_data, val_data, test_data

def create_sequences(data, seq_length):
    """Create sequences from the time series data."""
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def series_data(df, start_year=None, end_year=None):
    # Ensure 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    # Drop unused columns
    columns_to_drop = ['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits', 'Capital Gains']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    # Filter data within the specified year range
    if start_year is not None and end_year is not None:
        filtered_data = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    else:
        filtered_data = df
    
    # Set 'Date' as index
    filtered_data.set_index('Date', inplace=True)
    
    return filtered_data["Close"]






