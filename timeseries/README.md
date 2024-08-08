VOO Price Prediction using LSTM
This project demonstrates how to predict stock prices using an LSTM model. The main script loads historical data, preprocesses it, splits it into training and testing sets, creates sequences for the LSTM model, builds and trains the model, makes predictions, and evaluates the model's performance.

Table of Contents
Installation
Usage
Project Structure
Explanation
Contributing
License
Installation

Usage
Usage
1. Prepare your data:

Place your historical data CSV file in the data directory. Ensure the file is named voo_historical_data.csv or update the file_path variable in the main function.

2. Run the main script:

python main.py

This will execute the entire pipeline, from data loading and preprocessing to model training and evaluation.

Project Structure
graphql
Copy code
├── data
│   └── VOO_historical_data.csv      # Your historical data file
├── data_loader.py                   # Module for loading data
├── preprocessing.py                 # Module for preprocessing data
├── model.py                         # Module for building and training the LSTM model
├── utils.py                         # Utility functions for evaluation
├── plotting.py                      # Module for plotting predictions
├── main.py                          # Main script to run the project
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
Explanation
Main Script (main.py)
The main script orchestrates the entire workflow:

Load and preprocess the data:

data_loader.py contains the load_data function to load the historical data.
preprocessing.py includes the preprocess_data function to scale the data and split_data to split the dataset into training and testing sets.
Create sequences:

preprocessing.py also contains the create_sequences function to create sequences for the LSTM model.
Build and train the model:

model.py includes the build_model function to define the LSTM model architecture and the train_model function to train the model.
Make predictions:

The model makes predictions on both the training and testing datasets.
Inverse transform to get actual prices:

The predicted values are inverse transformed to their original scale.
Plot predictions:

plotting.py contains the plot_predictions function to visualize the actual vs. predicted prices.
Evaluate model:

utils.py includes the evaluate_model function to calculate and print evaluation metrics.

Contributing
Feel free to submit issues or pull requests if you have suggestions for improvements or find bugs.

License
