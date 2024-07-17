import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_data(data):
    """Normalize the 'Close' prices in the data."""
    close_prices = data['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)
    return scaled_data, scaler

def split_data(scaled_data, train_ratio=0.8):
    """Split the data into training and testing sets."""
    train_size = int(len(scaled_data) * train_ratio)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size:]
    return train_data, test_data

def create_sequences(data, seq_length):
    """Create sequences from the time series data."""
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def series_data(df):
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.date
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df = df.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits', 'Capital Gains'], axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df["Close"]






