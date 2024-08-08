from data_loader import load_data
from preprocessing import series_data
from utils import *
from plotting import *
from model import *

file_path = 'data\voo_historical_data.csv' 
df = load_data(file_path)
    
    # Preprocess the data
ser = series_data(df)
    

log_ret = calc_log_ret(ser)

# Fit the ARIMA model
train_size = int(len(log_ret) * 0.8)
train, test = log_ret[:train_size], log_ret[train_size:]
    
#arima_order = (5, 0,5)
#model_fit = fit_arima_model(train, order=arima_order)
arima_order = (7, 0,7)
model_fit = fit_arima_model(train, order=arima_order)    

# Make predictions
predictions = model_fit.forecast(steps=len(test))
predictions.index = test.index     
    # Convert predictions to actual values
initial_value = ser.iloc[train_size]  # use the actual closing price before the test set
actual_predictions = log_ret_to_actual(predictions, initial_value)
    
    # Convert the actual test log returns to actual values
initial_train_value = ser.iloc[0]
test_actual_values = log_ret_to_actual(test, initial_value)
train_actual_values = log_ret_to_actual(train, initial_train_value)
    
    # Evaluate the model
mse, rmse = evaluate_arima_model(test, predictions)
print(f'MSE: {mse}, RMSE: {rmse}')
    
    # Plot actual vs predicted values
plot_actual_vs_predicted(test, predictions, "Actual vs Predicted Prices")
plot_actual_vs_predicted_vs_original(train_actual_values,test_actual_values, actual_predictions, "Actual vs Predicted Prices")