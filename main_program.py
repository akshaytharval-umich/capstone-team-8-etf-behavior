from NytScraper import scrape
from HuggingSentiment import analyze_sentiment
import pandas as pd
#scrape(holding='Facebook')

#model_name = "distilbert-base-uncased-finetuned-sst-2-english"
#model_name = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

# Sentiment Analysis Stage
# First load in articles.csv
df = pd.read_csv("articles.csv",encoding='utf-8',index_col=False)
new_df = analyze_sentiment(df,"lead_paragraph","distilbert-base-uncased-finetuned-sst-2-english")
# then save the df to csv
new_df.to_csv("articles.csv",encoding='utf-8',index=False)