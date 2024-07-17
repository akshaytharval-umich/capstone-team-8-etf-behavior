from data_loader import load_data
from preprocessing import series_data
from utils import *
from plotting import *

def main():
    # Load the data
    file_path = 'data\VOO_historical_data.csv' 
    df = load_data(file_path)
    
    # Preprocess the data
    close_series = series_data(df)
    
    # Plot historical closing prices
    plot_closing_prices(close_series)
    
    # Calculate and plot rolling statistics for closing prices
    wd_size = 5
    rolling_mean, rolling_std = calc_rolling_stats(close_series, wd_size)
    plot_rolling_stats(close_series, rolling_mean, rolling_std, wd_size, f"Daily VOO prices\nRolling Stats with Window Size = {wd_size} Days")
    
    # Calculate log returns
    log_ret = calc_log_ret(close_series)
    
    # Plot log returns and rolling statistics
    wd_size = 5
    rolling_mean, rolling_std = calc_rolling_stats(log_ret, wd_size)
    plot_rolling_stats(log_ret, rolling_mean, rolling_std, wd_size, f"Log Return of Daily VOO prices\nRolling Stats with Window Size = {wd_size} Days")
    
    # Test for stationarity
    test_stationarity(close_series)
    
    # Plot ACF
    plot_acf_series(close_series, max_lag=30)
    
    # Perform seasonal decomposition
    trend, seasonal, residual = perform_seasonal_decomposition(close_series)
    
    # Plot seasonal components
    plot_seasonal_components(close_series, trend, seasonal, residual)

if __name__ == "__main__":
    main()
