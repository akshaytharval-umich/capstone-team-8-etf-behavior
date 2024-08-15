# this function utilizes the answers from this stack overflow post
# https://stackoverflow.com/questions/37292872/how-can-i-one-hot-encode-in-python

import pandas as pd
import re
from datetime import datetime, timedelta
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt

def determine_col_lst(data):
    # get every column containing :label: and  holding
    column_names = [x for x in data.columns if ':label:' in x]
    column_names.append("holding")
    return column_names

def calc_one_hot_encode(data,column_names):
    # this function takes a dataframe and a name of the source column
    dummies_df = pd.get_dummies(data[column_names],dtype=int)
    # dummies_df is a separate dataframe where each column is one of the categorical values
    # then concat this with the original data column, similar to the stackoverflow post
    dummies_df = pd.concat([data,dummies_df],axis=1)
    # then we need to drop the column name, to avoid excess
    dummies_df = dummies_df.drop(column_names,axis=1)
    return dummies_df # and return the final conjoined dataframe

def scale_vectors(data):
    # This function works to split, apply, combine on a dataframe
    # from the CalcOneHotEncode function. It is grouped by days
    # and the vectors of sentiment and scaled by score are added

    score_regex = r":score:"
    label_regex = r":label:"
    scores_col_names = [column for column in data.columns if re.search(score_regex,column)]
    labels_col_names = [column for column in data.columns if re.search(label_regex,column)]

    # Then we need to loop through each scaling factor aka the scores
    for score_col_name in scores_col_names:
        # we need to find the matching label column names, based on source column and model name
        # regex pattern based off this post: https://stackoverflow.com/questions/7124778/how-can-i-match-anything-up-until-this-sequence-of-characters-in-a-regular-exp
        score_filter_pattern = r"^(.*?):[^:]*:(.*)$"
        results = re.match(score_filter_pattern,score_col_name)
        # splice out groups according to: https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/
        source_column = results.group(1)
        model_name = results.group(2)
        match_label_col_names_pattern = rf"^{source_column}:label:{model_name}_*"
        # then find the matching columns in labels
        matching_label_column_names = [name for name in labels_col_names if re.search(match_label_col_names_pattern,name)]
        print("----")
        print(score_col_name)
        print(matching_label_column_names)
        # then we need to vector multiply
        for label_col_name in matching_label_column_names:
            data[label_col_name] = data[score_col_name] * data[label_col_name]
        data = data.drop(score_col_name,axis=1)
    return data

# First is to filter down to the important fields pub_date, :label:, holding_
def group_apply_reduce(data):
    # The goal of this function is to group the dataframe by date and sum the vectors of label and holding
    col_lst = ['pub_date']
    label_lst = [x for x in data.columns if ':label:' in x]
    col_lst.extend(label_lst)
    hold_lst = [x for x in data.columns if 'holding_' in x]
    col_lst.extend(hold_lst)
    # now select the relevant columns
    df = data[col_lst]
    # made a dictionary for an aggregation, want the average sentiment score, and how many queries it got hits for
    agg_dict = {}
    for label in label_lst:
        agg_dict[label] = "mean"
    for holding in hold_lst:
        agg_dict[holding] = "sum"
    # Then convert 'pub_date' to datetime object. source: 
    # https://www.tutorialspoint.com/how-to-group-pandas-dataframe-by-date-and-time#:~:text=We%20use%20the%20groupby(),procedure%20on%20the%20assembled%20information.
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    # then perform groupby
    df = df.groupby(pd.Grouper(key="pub_date",freq="D")).agg(agg_dict)
    return df

def join_voo_data(data,voo_data):
    # Scaffolding with chatgpt
    # This is a function that joins the embedded and analyzed articles, with the historical data from VOO
    # looking at the v00 data, and the processed data, we only care if it happened on the same day
    # issues with different time zones, set everything to utc
    # we also wanna keep all dates for now, so leave everything on join
    data.index = pd.to_datetime(data.index,utc=True)
    data.index = data.index.normalize()
    voo_data.index = pd.to_datetime(voo_data.index,utc=True)
    voo_data.index = voo_data.index.normalize()
    combined_df = data.join(voo_data, how="outer")
    # Eliminate days where the market is closed
    combined_df = combined_df[~combined_df['Open'].isnull()]
    # Forward fill days where holiday for news, but not the market
    combined_df = combined_df.ffill()
    return combined_df

def calc_etf_price_change(data,threshold):
    # Calculate etf_price__change
    data['etf_price_change'] = (data['Close'] - data['Open'])/data['Open']*100
    # with a set threshold, rate as neutral, positive, negative, with dataframe apply
    def percent_classification(percentage,threshold):
        if percentage  >= threshold:
            return 1 # since positive
        elif percentage <= -threshold:
            # negative threshold, consider threshold a band on both sides to capture noise
            return -1
        else:
            return 0 # it's noise
    column_name = f"ground_truth_{threshold}%"
    data[column_name] = data['etf_price_change'].apply(percent_classification,threshold=threshold)
    return data,column_name

def time_shift(data_path):
    # the purpose of this function is to shift weekends to Monday, to capture weekend sentiment
    df = pd.read_csv(data_path,encoding='utf-8',index_col=False)
    # cast to date time
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    for index, row in df.iterrows():
        if row['pub_date'].weekday()==5:
            # its 0 indexed, so 5 is saturday, 6 is sunday
            df.at[index,'pub_date'] = row['pub_date'] + timedelta(days=2)
        elif row['pub_date'].weekday()==6:
            # only add 1 day since its Sunday
            df.at[index,'pub_date'] = row['pub_date'] + timedelta(days=1)
    return df

def compare_ground_truth(data_path, model_names,column_names,ground_labels):
    # this takes the output of join_voo_data and determines whether sentiment correlates strongly with movement
    def parse_label(string_label):
        # internal function to parse state from end of label
        lst = string_label.split('_')
        state = lst[-1].lower() # should be the last part of a 3 element list
        if state == "positive":
            return 1
        elif state == "neutral":
            return 0
        else:
            return -1
    df = pd.read_csv(data_path,encoding='utf-8',index_col=0)
    # model_names is a list of the hugging face models
    model_lst = []
    for source_column in column_names:
        for model_name in model_names:
            label_regex=rf"^{source_column}:label:{model_name}_"
            columns = df.filter(regex=label_regex).columns
            # can use idxmax according to https://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.idxmax.html
            highest_score_label = df[columns].idxmax(axis=1)
            # highest_scoree_label contains the column name of the highest value, parse the state at the end after _ with a  split
            col_name = f"{source_column}:{model_name}_Prediction"
            model_lst.append(col_name)
            df[col_name] = highest_score_label.apply(parse_label)
    # with the df, create a new results dataframe
    column_names = [column for column in column_names if 'ground_truth' in column]
    f1_results = pd.DataFrame(index=model_lst,columns=column_names)
    accuracy_results = pd.DataFrame(index=model_lst,columns=column_names)
    best_acc = 0
    best_acc_model = None
    for model_label in model_lst:
        for ground_label in ground_labels:
            # compare both data series with sklearn, easier then by hand
            f1_score = metrics.f1_score(df[ground_label],df[model_label],average='macro')
            f1_results.at[model_label,ground_label] = f1_score
            accuracy = metrics.accuracy_score(df[ground_label],df[model_label])
            accuracy_results.at[model_label,ground_label] = accuracy
            # optimized for accuracy, best metric
            if accuracy > best_acc:
                best_acc = accuracy
                best_acc_model = (ground_label,model_label)
    f1_results.to_csv('sentiment_analysis_huggingface/f1_scores.csv',index=True)
    accuracy_results.to_csv("sentiment_analysis_huggingface/accuracy_scores.csv",index=True)
    # reference: https://www.w3schools.com/python/python_ml_confusion_matrix.asp
    matrix = confusion_matrix(df[ground_label],df[model_label],labels=[1,0,-1])
    confusion_matrix_dis = metrics.ConfusionMatrixDisplay(confusion_matrix=matrix,display_labels=['Positive','Neutral','Negative'])
    confusion_matrix_dis.plot().figure_.savefig('sentiment_analysis_huggingface/confusion_matrix.png')


def split_frame(data_path,percent_test=None,span_test = None):
    # given data and a percentage or a time delta object, return two dataframes
    df = pd.read_csv(data_path,encoding='utf-8',index_col=0)
    start_date = df.index[0]
    last_date = df.index[-1]
    print(len(df.index))
    if percent_test != None:
        # then take a percentage for the test
        slice = int(len(df.index)*percent_test)
        test_index = df.index[-slice]
    print(start_date)
    print(last_date)