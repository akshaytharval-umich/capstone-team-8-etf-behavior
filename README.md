# capstone-team-8-etf-behavior

### UMich MADS SIADS 699 Capstone Team 8
---

# VOO ETF Price behavior Prediction Project

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

## Usage

### 1. Prepare Your Data
Place your historical data CSV file in the `data` directory. Ensure the file is named `voo_historical_data.csv`, or update the `file_path` variable in the script.

### 2. Run the Main Script

#### LSTM Model:
```bash
python main.py
```
This will execute the LSTM model pipeline, from data loading and preprocessing to model training and evaluation.

#### ARIMA Model:
```bash
python arima_modelmain.py
```
This will execute the ARIMA model pipeline, from data loading and preprocessing to model training and evaluation.

#### Exploratory Data Analysis (EDA):
```bash
python exploredatamain.py
```
This will execute the EDA pipeline of the time series analysis.

## Financial News Summarization and Sentiment Analysis

This component processes financial news articles to generate summaries, assess sentiment towards specific companies, and evaluate the relevance of each article using the OpenAI API. The enriched dataset can be used for building a sentiment analysis model.

### Extracting News Articles from the New York Times API

#### Setup:
1. Clone this repository.
2. Run the following command for the holding name of a company (holding name must be one of the companies in `API_Rules.py`):
   ```python
   from NytScraper import scrape
   scrape('Meta')
   ```
   Repeat the process until the scraping completes. If scraping stops due to API throttling, restart the next day.

#### Input:
- Holding name from `API_Rules.py` (additional companies can be added as needed).

#### Output:
- CSV file with articles.
- Helper CSV file representing news articles from which holding is extracted.

## Project Overview

The script reads a CSV file containing financial news articles, cleans the data by removing entries with missing text, and ensures that all entries in the `LLM_Output` column are in string format. It then processes each article with the OpenAI model to:

- Generate a five-line summary.
- Determine sentiment (Positive/Negative) towards a specific company.
- Assess the relevance of the article to the company.

The generated output is stored in the dataset for further analysis or modeling.

## Requirements

- Python 3.x
- pandas
- tqdm
- openai
- HuggingFace Transformers
- Additional custom modules: `NytScraper`, `HuggingSentiment`, `DataPrepUtils`

### Installation:
```bash
pip install pandas tqdm openai transformers
```

## Setup

1. Clone this repository or download the script.
2. Ensure you have a CSV file named `articles_full.csv` in the working directory containing a `full_article` column with the content of the articles and a `holding` column with the company names.
3. Obtain an OpenAI API key and replace `{YOUR_KEY}` in the script with your actual API key.

## Usage

### 1. Run the Script
```bash
python financial_news_summary.py
```
The script will process the articles, generate summaries, sentiment, and relevance, and store the output in the `LLM_Output` column of the dataset.

### Output

- **LLM_Output:** This column contains the AI-generated summaries, sentiment, and relevance for each article. The output format is:
  - **Summary:** <Summary of the article in 5 lines>
  - **Overall sentiment:** <Positive or Negative>
  - **Relevance to company:** <High, Low, or NA>
  - **Company Name:** <Company provided>

---

## Sentiment Analysis and VOO ETF Price Prediction

This project analyzes the sentiment of financial news articles using pre-trained NLP models and evaluates the impact of these sentiments on VOO ETF price changes. The project involves several stages, from scraping and sentiment analysis to data preparation and evaluation.

### Steps:

1. **Scrape Financial News Articles:** 
   - Use the `NytScraper` module (not included in the provided script).
  
2. **Sentiment Analysis:** 
   - Analyze the sentiment of different parts of the articles (abstract, lead_paragraph, full_text) using pre-trained NLP models.

3. **Data Preparation:** 
   - Pre-process the articles by one-hot encoding, scaling vectors, time-shifting, and grouping the data.

4. **Joining VOO ETF Data:** 
   - Combine the sentiment analysis data with VOO historical price data to assess the impact of news sentiment on price changes.

5. **Price Change Calculation:** 
   - Evaluate the price change based on specific thresholds and generate ground truth data.

6. **Evaluation:** 
   - Compare the ground truth with the model predictions and split the dataset for testing and evaluation.

### Setup

1. Clone this repository or download the script.
2. Ensure you have the required data files:
   - `complete_raw_articles.csv`: Contains the full text of financial news articles.
   - `VOO_historical_data.csv`: Contains the historical price data for VOO ETF.
   - (Optional) `articles_sentiment.csv`, `articles_encoded.csv`, `articles_scaled.csv`, `articles_shifted.csv`, `articles_grouped.csv`: Intermediate processed files.
3. Make sure you have the custom modules (`NytScraper`, `HuggingSentiment`, `DataPrepUtils`) available in your project directory.

### Usage

1. **Sentiment Analysis:** 
   Uncomment the relevant sections in the script to perform sentiment analysis on the articles using different models. The script will save the results in `articles_sentiment.csv`.

2. **Data Preparation:** 
   Pre-process the data by one-hot encoding, scaling, time-shifting, and grouping. These steps will prepare the data for joining with VOO ETF data.

3. **Join with VOO Data:** 
   Combine the sentiment data with the VOO historical data and calculate the price change with specified thresholds.

4. **Evaluation:** 
   Evaluate the ground truth against model predictions and split the data for testing.

### Output

- **articles_sentiment.csv:** Contains the sentiment analysis results.
- **articles_encoded.csv:** One-hot encoded sentiment data.
- **articles_scaled.csv:** Scaled sentiment data.
- **articles_shifted.csv:** Time-shifted data to adjust for weekends and holidays.
- **articles_grouped.csv:** Grouped data for analysis.
- **articles_voo.csv:** Combined sentiment and VOO data with calculated price changes.
- **articles_ground_comparison.csv:** Evaluation results comparing ground truth with model predictions.

---

## Data Access Statement

The data used in this project is sourced from [yfinance](https://www.yfinance.com) for financial information and [New York Times](https://www.nytimes.com) news articles for textual data. Access to this data is subject to the respective terms of service and licensing agreements of the data providers. Please ensure compliance with these licenses when using or redistributing the data.

--- 

