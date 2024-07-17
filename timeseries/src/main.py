import numpy as np
from data_loader import load_data
from preprocessing import preprocess_data, split_data, create_sequences
from model import build_model, train_model
from utils import evaluate_model
from plotting import plot_predictions

def main(file_path, seq_length=60, epochs=20, batch_size=32, train_ratio=0.8):
    # Load and preprocess the data
    data = load_data(file_path)
    scaled_data, scaler = preprocess_data(data)
    
    # Split the data into training and testing sets
    train_data, test_data = split_data(scaled_data, train_ratio)
    
    # Create sequences
    X_train, y_train = create_sequences(train_data, seq_length)
    X_test, y_test = create_sequences(test_data, seq_length)
    
    # Reshape for LSTM input
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    
    # Build and train the model
    model = build_model((seq_length, 1))
    model = train_model(model, X_train, y_train, epochs, batch_size)
    
    # Make predictions
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)
    
    # Inverse transform to get actual prices
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    y_train_actual = scaler.inverse_transform(y_train.reshape(-1, 1))
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Plot predictions
    plot_predictions(y_test_actual, test_predict, 'VOO Price Prediction')
    
    # Evaluate model
    evaluate_model(y_test_actual, test_predict)

# Run the main function
if __name__ == "__main__":
    file_path = 'data\VOO_historical_data.csv'  # Replace with your actual file path
    main(file_path)
