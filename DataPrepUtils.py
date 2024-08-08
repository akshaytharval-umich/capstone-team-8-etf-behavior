# this function utilizes the answers from this stack overflow post
# https://stackoverflow.com/questions/37292872/how-can-i-one-hot-encode-in-python

import pandas as pd
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


#def group_reduce(data,):
    # This function works to split, apply, combine on a dataframe
    # from the CalcOneHotEncode function. It is grouped by days
    # and the vectors of sentiment and scaled by score are added

    # calc_one_hot_encode should be run several times before this stage
    # first step after one hot encoding is to 

