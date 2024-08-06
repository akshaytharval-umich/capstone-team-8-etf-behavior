from NytScraper import scrape
from HuggingSentiment import analyze_sentiment
import pandas as pd
scrape(holding='Meta')

""" model_dist_bert = "distilbert-base-uncased-finetuned-sst-2-english"
model_dist_fin = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

model_names = [model_dist_bert,model_dist_fin]

# Sentiment Analysis Stage
# First load in articles.csv
df = pd.read_csv("articles.csv",encoding='utf-8',index_col=False)
for model_name in model_names:
    df = analyze_sentiment(df,"abstract",model_name)
# then save the df to csv
df.to_csv("articles.csv",encoding='utf-8',index=False) """