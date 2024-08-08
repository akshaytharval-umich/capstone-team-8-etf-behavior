# this function utilizes the answers from this stack overflow post
# https://stackoverflow.com/questions/37292872/how-can-i-one-hot-encode-in-python

import pandas as pd
import re
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
    print(scores_col_names)
    print(labels_col_names)

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
        for label_col_name in labels_col_names:
            data[label_col_name] = data[score_col_name] * data[label_col_name]
        data = data.drop(score_col_name,axis=1)
    return data