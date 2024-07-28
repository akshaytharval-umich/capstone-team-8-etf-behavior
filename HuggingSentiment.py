# Reference for gpu usage: https://discuss.huggingface.co/t/is-transformers-using-gpu-by-default/8500
# Reference for setup: https://www.youtube.com/watch?v=GSt00_-0ncQ
# reference for arguments and examples: https://huggingface.co/docs/transformers/en/main_classes/pipelines
# https://huggingface.co/docs/transformers/en/quicktour

from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification # Comes from model documentation
import torch
import torch.nn.functional as F

def analyze_sentiment(data,source_name,model_name):
    # this function takes several parameters
    # text_lst, this is a series of strings from the dataframe, typically either the lead paragraph or full text

    # Next check if a gpu is available
    device ="cuda:0" if torch.cuda.is_available() else "cpu"

    # retrieve pretrained model
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    # and the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # and the classifier
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer,device=0)
    # First let's handle NaNs in the source data column, get indices of real values
    df_index = data[data[source_name].notnull()].index
    # Feed it the column of the source name
    lst = data.loc[data.index[df_index],source_name].tolist()

    lst_dicts = classifier(lst)
    print("made it")
    # As a list of dictionaries, need to move the two scores, withh comprehension
    labels = [result_dict['label'] for result_dict in lst_dicts]
    scores = [result_dict['score'] for result_dict in lst_dicts]
    # create the new name of the column from the model name
    label_name = source_name + ":" + "label" + ":" + model_name
    scores_name = source_name + ":" + "score" + ":" + model_name

    data[label_name] = ""
    data.loc[data.index[df_index],label_name] = labels

    data[scores_name] = ""
    data.loc[data.index[df_index],scores_name] = scores

    return data

