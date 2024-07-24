# Need pandas
import pandas as pd
import time
from datetime import datetime
from newspaper import Article

test_time = 13 #technically 12, but hit a bad permission

def extract_full_text(csv_path):
    # Extracts the full text using the pip install newspaper3k
    
    # First load in articles.csv
    df = pd.read_csv(csv_path,encoding='utf-8',index_col=False)

    # Does the articles column exist in the dataframe?
    if 'full_text' not in df.columns:
        df['full_text'] = ""
    
    # source: https://stackoverflow.com/questions/16476924/how-can-i-iterate-over-rows-in-a-pandas-dataframe
    df_filt = df.iloc[50:100]
    for index,row in df_filt.iterrows():
        # hold off for the timer
        print(index)
        time.sleep(test_time)
        url = row['web_url']
        article=Article(url)
        article.download()
        article.parse()
        full_text = article.text
        if full_text is not None:
            # pandas cheat sheet, address through .at and column
            df.at[index,'full_text'] = full_text
    
    # then save the df to csv
    df.to_csv("articles.csv",encoding='utf-8',index=False)
                
extract_full_text("articles.csv")