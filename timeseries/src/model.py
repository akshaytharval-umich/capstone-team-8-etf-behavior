#import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from keras.callbacks import EarlyStopping
import numpy as np

def build_model(input_shape):
    """Build the LSTM model."""
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, X_train, y_train,X_val, y_val, epochs, batch_size):
    """Train the LSTM model with early stopping."""
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    model.fit(
        X_train, 
        y_train, 
        epochs=epochs, 
        batch_size=batch_size, 
        validation_data=(X_val, y_val), 
        callbacks=[early_stopping]
    )
    return model


def fit_arima_model(series, order=(5, 0, 5)):
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    return model_fit

def forecast_arima_model(model_fit, steps=5):
    forecast = model_fit.forecast(steps=steps)
    return forecast

def evaluate_arima_model(test_series, predictions):
    mse = mean_squared_error(test_series, predictions)
    rmse = np.sqrt(mse)
    return mse, rmse