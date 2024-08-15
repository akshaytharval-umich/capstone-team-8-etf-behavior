from NytScraper import scrape
from HuggingSentiment import analyze_sentiment
import DataPrepUtils as utils
import pandas as pd

model_dist_bert = "distilbert-base-uncased-finetuned-sst-2-english"
model_dist_fin = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
model_finbert = "ProsusAI/finbert"

model_names = [model_dist_bert,model_dist_fin,model_finbert]
column_names = ['abstract','lead_paragraph','full_text']

# Sentiment Analysis Stage
# First load in articles.csv "full_text"
df = pd.read_csv("csentiment_analysis_huggingface/omplete_raw_articles.csv",encoding='utf-8',index_col=False)
for column_name in column_names:
    for model_name in model_names:
        df = analyze_sentiment(df,column_name,model_name)
#then save the df to csv
df.to_csv("sentiment_analysis_huggingface/articles_sentiment.csv",encoding='utf-8',index=False)

df = pd.read_csv("sentiment_analysis_huggingface/articles_sentiment.csv",encoding='utf-8',index_col=False)
column_lst = utils.determine_col_lst(df)

encoded_df = utils.calc_one_hot_encode(df,column_lst)
encoded_df.to_csv("sentiment_analysis_huggingface/articles_encoded.csv",encoding='utf-8',index=False)

# Next pre-processing before grouping
df = pd.read_csv("sentiment_analysis_huggingface/articles_encoded.csv",encoding='utf-8',index_col=False)
new_df = utils.scale_vectors(df)
new_df.to_csv("sentiment_analysis_huggingface/articles_scaled.csv",encoding='utf-8',index=False)

# Next timeshift the weekends
df = utils.time_shift("sentiment_analysis_huggingface/articles_scaled.csv")
df.to_csv("sentiment_analysis_huggingface/articles_shifted.csv",encoding='utf-8',index=True)

df = pd.read_csv("sentiment_analysis_huggingface/articles_shifted.csv",encoding='utf-8',index_col=False)
df = utils.group_apply_reduce(df)
df.to_csv("sentiment_analysis_huggingface/articles_grouped.csv",encoding='utf-8',index=True)

df = pd.read_csv("sentiment_analysis_huggingface/articles_grouped.csv",encoding='utf-8',index_col='pub_date')
voo = pd.read_csv("sentiment_analysis_huggingface/VOO_historical_data.csv",encoding='utf-8',index_col='Date')
combined_df = utils.join_voo_data(df,voo) 
# Then calculate the price change w/ threshold in %
thresholds = [0.1,0.2,0.3,0.4]
ground_truth_labels = []
for percentage in thresholds:
    combined_df,col = utils.calc_etf_price_change(combined_df,threshold=percentage)
    ground_truth_labels.append(col)
combined_df.to_csv("sentiment_analysis_huggingface/articles_voo.csv",encoding='utf-8',index=True)

# Evaluation of ground truth versus movement, compare ground truth
df = utils.compare_ground_truth("sentiment_analysis_huggingface/articles_voo.csv",model_names,column_names,ground_truth_labels)