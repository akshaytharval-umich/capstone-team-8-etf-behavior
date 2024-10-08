import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.seasonal import seasonal_decompose



sns.set(style='whitegrid')


def plot_predictions(y_actual, y_predicted, title):
    """Plot the actual vs predicted VOO prices."""
    plt.figure(figsize=(14, 5))
    plt.plot(y_actual, color='blue', label='Actual VOO Price')
    plt.plot(y_predicted, color='red', label='Predicted VOO Price')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('VOO Price')
    plt.legend()
    plt.show()


def plot_rolling_stats(series, rolling_mean, rolling_std, wd_size, title):
    """Plot rolling statistics."""
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(series, label="Original")
    ax.plot(pd.Series(rolling_mean, index=series.index), label="Rolling Mean")
    ax.plot(pd.Series(rolling_std, index=series.index), label="Rolling Std")
    ax.set_xlabel("Day")
    ax.set_ylabel("Close Price")
    ax.set_title(title)
    ax.legend()
    plt.show()


def plot_closing_prices(series):
    """Plot historical closing prices."""
    plt.figure(figsize=(14, 7))
    plt.plot(series.index, series.values, label='Close Price')
    plt.title('VOO Historical Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.show()

def plot_acf_series(ser, max_lag):
    """Plot the autocorrelation function."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    plot_acf(ser, ax=ax, lags=max_lag, title="Daily VOO prices\nAutocorrelation Function")
    ax.set_xlabel("Lag")
    ax.set_ylabel("Correlation")
    plt.show()

def perform_seasonal_decomposition(series, period=252):
     
    """Perform seasonal decomposition."""
    
    result = seasonal_decompose(series, model='multiplicative', period=period) 
    
    # Plot the decomposition
    plt.figure(figsize=(24, 18))
    result.plot()
    plt.show()
    
    return result.trend, result.seasonal, result.resid

def plot_seasonal_components(series, trend, seasonal, residual):
    """Plot seasonal components."""
    plt.figure(figsize=(14, 10))

    plt.subplot(411)
    plt.plot(series, label='Original', color='blue')
    plt.legend(loc='upper left')

    plt.subplot(412)
    plt.plot(trend, label='Trend', color='red')
    plt.legend(loc='upper left')

    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality', color='green')
    plt.legend(loc='upper left')

    plt.subplot(414)
    plt.plot(residual, label='Residuals', color='purple')
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()

def plot_actual_vs_predicted_vs_original(train, actual, predicted, title):
    """
    Plots the original training data, actual values, and predicted values.

    Parameters:
    - train: pd.Series, original training data
    - actual: pd.Series, actual values for the test set
    - predicted: pd.Series, predicted values for the test set
    - title: str, title of the plot
    """
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot the original training data
    ax.plot(train, label="Original")
    
    # Concatenate the last value of the training set with the actual values
    actual_concat = pd.concat([train[-1:], actual])
    
    # Concatenate the last value of the training set with the predicted values
    predicted_concat = pd.concat([train[-1:], predicted])
    
    # Plot the actual and predicted values
    ax.plot(actual_concat, label='Actual')
    ax.plot(predicted_concat, label='Predicted', linestyle='--')
    
    # Set the labels and title
    ax.set_xlabel("Date")
    ax.set_title(title)
    ax.legend()
    
    # Display the plot
    plt.show()

  
def plot_actual_vs_predicted(actual, predicted, title):
    """Plot actual vs predicted values."""
    plt.figure(figsize=(14, 7))
    plt.plot(actual, label='Actual')
    plt.plot(predicted, label='Predicted', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.legend()
    plt.xticks(rotation=45)
    plt.title(title)
    plt.show()



 