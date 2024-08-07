# this function utilizes the answers from this stack overflow post
# https://stackoverflow.com/questions/37292872/how-can-i-one-hot-encode-in-python
# and the api for including a prefix
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.add_prefix.html

import pandas as pd

def calc_one_hot_encode(data,column_name):
    # this function takes a dataframe and a name of the source column
    dummies_df = pd.get_dummies(data[[column_name]])
    # dummies_df is a separate dataframe where each column is one of the categorical values
    # the goal then is to rename each column with the preface of the column name
    dummies_df = dummies_df.add_prefix(column_name)
    # then concat this with the original data column, similar to the stackoverflow post
    dummies_df = pd.concat([data,dummies_df])
    # then we need to drop the column name, to avoid excess
    dummies_df = dummies_df.drop(column_name,axis=1)
    return dummies_df # and return the final conjoined dataframe
