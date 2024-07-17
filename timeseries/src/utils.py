import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import matplotlib.dates as mdates
import pandas as pd
import numpy as np


def evaluate_model(y_actual, y_predicted):
    """Evaluate the model performance."""
    mse = mean_squared_error(y_actual, y_predicted)
    mae = mean_absolute_error(y_actual, y_predicted)
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    return mse, mae

def calc_rolling_stats(ser, wd_size=7):
    arr_w = np.ones(wd_size)
    rolling_mean = np.array([np.average(ser.iloc[max(0, x - wd_size + 1):x + 1], weights=arr_w[-(x + 1 - max(0, x - wd_size + 1)):]) for x in range(len(ser))])
    rolling_std = np.sqrt(np.array([np.average((ser.iloc[max(0, x - wd_size + 1):x + 1] - rolling_mean[x])**2, weights=arr_w[-(x + 1 - max(0, x - wd_size + 1)):]) for x in range(len(ser))]))
    return rolling_mean, rolling_std

def calc_log_ret(ser):
    log_ret = np.log(ser / ser.shift(1)).dropna()
    log_ret.index = pd.to_datetime(log_ret.index)
    return log_ret

def test_stationarity(data):
    result = adfuller(data, autolag='AIC')
    print('Results of Dickey-Fuller Test:')
    dfoutput = pd.Series(result[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in result[4].items():
        dfoutput[f'Critical Value ({key})'] = value
    print(dfoutput)

def calc_acf(ser, max_lag):
    ans_acf = sm.tsa.acf(ser, nlags=max_lag)
    return ans_acf


def log_ret_to_actual(log_ret, initial_value):
    """
    Converts log returns back to actual values.
    
    Parameters:
    log_ret (pd.Series): A series of log returns.
    initial_value (float): The initial value of the series.
    
    Returns:
    pd.Series: A series of actual values.
    """
    # Compute the cumulative sum of log returns
    cum_log_ret = log_ret.cumsum()
    
    # Exponentiate the cumulative log returns and multiply by the initial value
    actual_values = np.exp(cum_log_ret) * initial_value
    
    return actual_values