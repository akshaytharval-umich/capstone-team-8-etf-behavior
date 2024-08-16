### UMich MADS SIADS 699 Capstone Team 8
---
# Topic: VOO ETF Price Behavior Prediction Project

## Introduction


This project aims to predict the behavior of the VOO ETF by leveraging a dual approach: analyzing comprehensive historical time series data and performing sentiment analysis on news articles related to its top 10 holdings.

## Time Series Analysis and Modeling

The main script handles the following tasks:
- **Data Loading:** Import historical data.
- **Preprocessing:** Clean and prepare the data.
- **Data Splitting:** Divide data into training and testing sets.
- **Sequence Creation:** Generate sequences for the LSTM model.
- **Model Training:** Build and train the model.
- **Prediction & Evaluation:** Make predictions and evaluate model performance.

### Usage
---

#### 1. Prepare Your Data
Place your historical data CSV file in the `data` directory. Ensure the file is named `voo_historical_data.csv`, or update the `file_path` variable in the script.

#### 2. Run the Main Script

##### LSTM Model:
```bash
python main.py
```
This will execute the LSTM model pipeline, from data loading and preprocessing to model training and evaluation.

##### ARIMA Model:
```bash
python arima_modelmain.py
```
This will execute the ARIMA model pipeline, from data loading and preprocessing to model training and evaluation.

##### Exploratory Data Analysis (EDA):
```bash
python exploredatamain.py
```
This will execute the EDA pipeline of the time series analysis.

## Financial News Summarization and Sentiment Analysis

For financial news articles, we have used New York Times (NYT) API to get company (or holding) specific articles. From these articles, we have performed two independent experiments, first training a huggingface model using full news articles and structured LLM summary outputs, second using off the shelf model from hugging face for sentiment analysis of leading paragraphs.
Initial extraction of news articles from NYT API remains the same

### Extracting News Articles from the New York Times API
---
#### Setup:
1. Clone this repository.
2. Run the following command for the holding name of a company (holding name must be one of the companies in `API_Rules.py`):
   ```python
   from NytScraper import scrape
   scrape('Meta')
   ```
   Repeat the process until the scraping completes. If scraping stops due to API throttling, restart the next day.
   At the end of each run, open the datamanager.csv generated to check the progress and outstanding api calls that need to be made.

#### Input:
- Holding name from `API_Rules.py` (additional companies can be added as needed).

#### Output:
- CSV file with articles.
- Helper CSV file representing news articles from which holding is extracted.

### Sentiment Analysis Model using LLM summary and full articles
---
For this experiment, you will need to follow these steps:
1. Extract full articles
2. Get structured output from OpenAI's LLM
3. Prepare data for training
4. Make visuals (optional)
5. Train sentiment analysis model

#### 1. Extract full articles:
(Assuming the above steps for Extracting News Articles from NYT API are complete)
- Setup:
```bash
pip install pandas numpy newspaper3k matplotlib
```
- Run the notebook called `Extract_News_Articles.ipynb`, change the name of the file being read if required
- Output will be a csv file called `full_articles.csv`

#### 2. Get Structured output from LLM:
(Assuming you have the full articles from above step and column called `full_articles` in it)
- Setup:
```bash
pip install pandas openai
```
Also replace `{YOUR_KEY}` with your actual key by following steps [here](https://github.com/openai/openai-python). For extracting information from full news articles, we just need column `full_articles` from the output csv above. Also, a manual step of adding new column `llm_output` with value `0` is needed so that if loop within script fails, it will start from where the last OpenAI call was made.
- Run the notebook called `OpenAi_Prompt_Engineering.ipynb`. We can also add more information extraction in prompt if required. Script will make sure to save a csv file every 100 iterations.
- Output will be a new csv file called `articles_with_llm.csv`

#### 3. Prepare data for training:
(Assuming you have run full news articles extraction and run LLM prompts on it)
- Setup:
```bash
pip install pandas
```
Make sure to have VOO price data (available in google drive, also mentioned above on how to extract)
`article_columns_filtered.csv` is a csv file with `pub_date` column (publishing date of the article), `full_article` column and `llm_output` column
- Run the notebook called `Build_Sentiment_analysis_Data.ipynb` notebook
- Output will be a new csv file called `Full_Data_Sentiment_Analysis_LLM_Output_ETF_value_Label.csv`

#### 4. Make Word Cloud visual:
(Assuming you have `Full_Data_Sentiment_Analysis_LLM_Output_ETF_value_Label.csv` available)
- Setup:
```bash
pip install pandas wordcloud matplotlib
```
- Run the script and it will save 2 images, one each for positive and negative labels
- Output will be 2 images for positive and negative labels

#### 5. Train sentiment analysis model:
(Assuming you have `Full_Data_Sentiment_Analysis_LLM_Output_ETF_value_Label.csv` available)
- Setup:
```bash
pip install pandas tqdm openai transformers scikit-learn newspaper3k
```
- Run `Train_Sentiment_Analysis.ipynb` notebook with following instructions
  - You can select either `TEXT_COLUMN` or `full_articles` to be the input for model
  - You can select any one of these models to be trained:
      - "distilbert-base-uncased"
      - "bert-base-uncased"
      - "roberta-base"
      - "albert-base-v2"
      - "xlnet-base-cased"
- Output will be a model trained and saved `financial_sentiment_analysis_model_{model_name}.pt`
---

### Sentiment Analysis and VOO ETF Price Prediction using pre-trained models

This project analyzes the sentiment of financial news articles using pre-trained NLP models and evaluates the impact of these sentiments on VOO ETF price changes. The project involves several stages, from scraping and sentiment analysis to data preparation and evaluation.

#### Steps:

1. **Scrape Financial News Articles:** 
   - Use the `NytScraper` module (not included in the provided script).
  
2. **Sentiment Analysis:** 
   - Analyze the sentiment of different parts of the articles (abstract, lead_paragraph, full_text) using pre-trained NLP models.
   - Run the following file `main_program.py` in the sentiment_analysis_huggingface directory. It will run the entire pipeline through evaluation. It may take several minutes to complete.

3. **Data Preparation:** 
   - Pre-process the articles by one-hot encoding, scaling vectors, time-shifting, and grouping the data.

4. **Joining VOO ETF Data:** 
   - Combine the sentiment analysis data with VOO historical price data to assess the impact of news sentiment on price changes.

5. **Price Change Calculation:** 
   - Evaluate the price change based on specific thresholds and generate ground truth data.

6. **Evaluation:** 
   - Compare the ground truth with the model predictions and split the dataset for testing and evaluation.

#### Setup

1. Clone this repository or download the script.
2. Ensure you have the required data files:
   - `complete_raw_articles.csv`: Contains the full text of financial news articles.
   - `VOO_historical_data.csv`: Contains the historical price data for VOO ETF.
   - (Optional) `articles_sentiment.csv`, `articles_encoded.csv`, `articles_scaled.csv`, `articles_shifted.csv`, `articles_grouped.csv`: Intermediate processed files.
3. Make sure you have the custom modules (`NytScraper`, `HuggingSentiment`, `DataPrepUtils`) available in your project directory.

#### Usage

1. **Sentiment Analysis:** 
   Uncomment the relevant sections in the script to perform sentiment analysis on the articles using different models. The script will save the results in `articles_sentiment.csv`.

2. **Data Preparation:** 
   Pre-process the data by one-hot encoding, scaling, time-shifting, and grouping. These steps will prepare the data for joining with VOO ETF data.

3. **Join with VOO Data:** 
   Combine the sentiment data with the VOO historical data and calculate the price change with specified thresholds.

4. **Evaluation:** 
   Evaluate the ground truth against model predictions and split the data for testing.

#### Output

- **articles_sentiment.csv:** Contains the sentiment analysis results.
- **articles_encoded.csv:** One-hot encoded sentiment data.
- **articles_scaled.csv:** Scaled sentiment data.
- **articles_shifted.csv:** Time-shifted data to adjust for weekends and holidays.
- **articles_grouped.csv:** Grouped data for analysis.
- **articles_voo.csv:** Combined sentiment and VOO data with calculated price changes.
- **articles_ground_comparison.csv:** Evaluation results comparing ground truth with model predictions.
- **accuracy_scores.csv:** Accuracy Scores Table of tested models and thresholds.
- **f1_scores.csv:** F1 Scores Table of tested models and thresholds.
- **confusion_matrix.png:** Plot of the confusion matrix of the best model.

---

## Data Access Statement

The data used in this project is sourced from [yfinance](https://www.yfinance.com) for financial information and [New York Times](https://www.nytimes.com) news articles for textual data. Access to this data is subject to the respective terms of service and licensing agreements of the data providers. Please ensure compliance with these licenses when using or redistributing the data.

--- 

