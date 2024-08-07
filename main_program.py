#from NytScraper import scrape
#from HuggingSentiment import analyze_sentiment
import DataPrepUtils as utils
import pandas as pd
#scrape(holding='Meta')

model_dist_bert = "distilbert-base-uncased-finetuned-sst-2-english"
model_dist_fin = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
model_finbert = "ProsusAI/finbert"

model_names = [model_dist_bert,model_dist_fin,model_finbert]

# Sentiment Analysis Stage
# First load in articles.csv "full_text"
#df = pd.read_csv("articles_sentiment_analysis.csv",encoding='utf-8',index_col=False)
#for model_name in model_names:
#    df = analyze_sentiment(df,"full_text",model_name)
#then save the df to csv
#df.to_csv("articles_sentiment_analysis.csv",encoding='utf-8',index=False)

#df = pd.read_csv("articles_sentiment_analysis.csv",encoding='utf-8',index_col=False)
#column_lst = utils.determine_col_lst(df)

#encoded_df = utils.calc_one_hot_encode(df,column_lst)
#print(encoded_df.columns)
#encoded_df.to_csv("articles_encoded.csv",encoding='utf-8',index=False)

# Next pre-processing before grouping
#df = pd.read_csv("articles_encoded.csv",encoding='utf-8',index_col=False)
#new_df = utils.scale_vectors(df)
#new_df.to_csv("test.csv",encoding='utf-8',index=False)

df = pd.read_csv("test.csv",encoding='utf-8',index_col=False)
df = utils.group_apply_reduce(df)
df.to_csv("new_test.csv",encoding='utf-8',index=True)