 
# capstone-team-8-etf-behavior
UMich MADS SIADS 699 Capstone Team 8

## Introduction:
This project aims to predict the behavior of the VOO ETF by leveraging a dual approach: analyzing comprehensive historical time series data and performing sentiment analysis on news articles related to its top 10 holdings.
 
## Time Series Analysis and Model
The main script loads historical data, preprocesses it, splits it into training and testing sets, creates sequences for the LSTM model, builds and trains the model, makes predictions, and evaluates the model's performance.


### Usage
#### 1. Prepare your data:

    Place your historical data CSV file in the data directory. Ensure the file is named voo_historical_data.csv or update the file_path variable in the main functions.

#### 2. Run the main script:

#####  LSTM Model
` python main.py  `
        This will execute the LSTM model pipeline, from data loading and preprocessing to model training and evaluation.
#####  ARIMA Model
`python arima_modelmain.py `
        This will execute the ARIMA model pipeline, from data loading and preprocessing to model training and evaluation
#####  Exploratory Data Analysis (EDA)
`python exploredatamain.py`
        This will execute the EDA pipeline of the Time series Analysis.



## Financial News Summarization and Sentiment Analysis
This project processes a dataset of financial news articles to generate summaries, assess sentiment towards specific companies, and evaluate the relevance of each article using the OpenAI API. The enriched dataset can be used for building a sentiment analysis model.

## Extracting news articles from New York Times API:

### Setup:
1. Clone this repository
2. Run the following for the holding name of a company (holding name needs to be one of the companies in `API_Rules.py`)
```
from NytScraper import scrape
scrape('Meta')
```
3. Run the above piece of code till the scrapping stops
4. There can be cases when scrapping stops due to throttling from NYT API, in that case, start again the next day

#### Input:
Holding name from `API_Rules.py` (you can also add more companies if needed)

#### Output:
Two CSV files:
1. CSV file with articles
2. Helper CSV file representing news articles from which holding is extracted


# PART I


## Project Overview
The script reads a CSV file containing financial news articles, cleans the data by removing any entries with missing text, and ensures that all entries in the LLM_Output column are in string format. It then iterates through each article, sending the content to the OpenAI model with a prompt designed to:

Generate a five-line summary.
Determine the sentiment (Positive/Negative) towards a specific company.
Assess the relevance of the article to the company.
The generated output is stored back in the dataset for further analysis or modeling.

## Requirements
* Python 3.x
* pandas
* tqdm
* openai
* HuggingFace Transformers
* Additional custom modules (NytScraper, HuggingSentiment, DataPrepUtils)

To install the required packages, run: 

`pip install pandas tqdm openai`
`pip install pandas transformers tqdm`

## Setup
#### 1. Clone this repository or download the script.
#### 2. Ensure you have a CSV file named 'articles_full.csv' in the working directory. This file should
contain a "full_article" column with the content of the articles and a 'holding' column with 
the company names.
#### 3.Obtain an OpenAI API key and replace '{YOUR_KEY}' in the script with your actual API key.

# Usage
#### 1. Run the script:
`python financial_news_summary.py`

#### 2. The script will process the articles, generate summaries, sentiment, and relevance, and store the output in the 'LLM_Output' column of the dataset.

## Output
#### LLM_Output:
This column contains the AI-generated summaries, sentiment, and relevance for each article.
The output format is as follows:

```Summary: <Summary of the article in 5 lines>
Overall sentiment: <Positive or Negative>
Relevance to company: <High, Low, or NA>
Company Name: <Company provided>
```
# PART II
##### This project analyzes the sentiment of financial news articles using pre-trained NLP models and evaluates the impact of these sentiments on the VOO ETF price changes. The project includes several stages, from scraping and sentiment analysis to data preparation and evaluation.

This part of the project performs the following steps:

#### 1. Scrape Financial News Articles:
 (Not included in the provided script) This step involves scraping articles using the `NytScraper` module.
#### 2. Sentiment Analysis: 
Use pre-trained NLP models to analyze the sentiment of different parts of the articles `(abstract, lead_paragraph, full_text)`.
#### 3. Data Preparation: 
Pre-process the articles by one-hot encoding, scaling vectors, time-shifting, and grouping the data.
#### 4. Joining VOO ETF Data: 
Combine the sentiment analysis data with VOO historical price data to assess the impact of news sentiment on price changes.
#### 5. Price Change Calculation: 
Evaluate the price change based on specific thresholds and generate ground truth data.
#### 6. Evaluation: 
Compare the ground truth with the model predictions and split the dataset for testing and evaluation.

# Setup
#### 1. Clone this repository or download the script.
#### 2. Ensure you have the required data files:

   * `complete_raw_articles.csv`: Contains the full text of financial news articles.

   * `VOO_historical_data.csv`: Contains the historical price data for VOO ETF.

   * (Optional) `articles_sentiment.csv`, `articles_encoded.csv`, `articles_scaled.csv`,
     `articles_shifted.csv`, `articles_grouped.csv`: Intermediate processed files.

#### 3. Make sure you have the custom modules (NytScraper, HuggingSentiment, DataPrepUtils) available in your project directory.

# Usage
#### 1. Sentiment Analysis:
Uncomment the relevant sections in the script to perform sentiment analysis on the articles using different models. The script will save the results in articles_sentiment.csv.

 `# df = analyze_sentiment(df, column_name, model_name)`

 `# df.to_csv("articles_sentiment.csv", encoding='utf-8', index=False)`

#### 2. Data Preparation:
Pre-process the data by one-hot encoding, scaling, time-shifting, and grouping. These steps will prepare the data for joining with VOO ETF data.

`# encoded_df = utils.calc_one_hot_encode(df, column_lst)`

`# new_df = utils.scale_vectors(df)`

`# df = utils.time_shift("articles_scaled.csv")`

`# df = utils.group_apply_reduce(df)`

#### 3. Join with VOO Data:
Combine the sentiment data with the VOO historical data and calculate the price change with specified thresholds.

`combined_df = utils.join_voo_data(df, voo)`

`combined_df = utils.calc_etf_price_change(combined_df, threshold=percentage)`

#### 4. Evaluation:
Evaluate the ground truth against model predictions and split the data for testing.

`df = utils.compare_ground_truth("articles_voo.csv", model_names, column_names)`

`utils.split_frame("articles_voo.csv", percent_test=0.20)`

# Output
`articles_sentiment.csv`: Contains the sentiment analysis results.

`articles_encoded.csv`: One-hot encoded sentiment data.

`articles_scaled.csv`: Scaled sentiment data.

`articles_shifted.csv`: Time-shifted data to adjust for weekends and holidays.

`articles_grouped.csv`: Grouped data for analysis.

`articles_voo.csv`: Combined sentiment and VOO data with calculated price changes.

`articles_ground_comparison.csv`: Evaluation results comparing ground truth with model predictions.