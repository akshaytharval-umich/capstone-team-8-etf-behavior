# Reference for gpu usage: https://discuss.huggingface.co/t/is-transformers-using-gpu-by-default/8500
# Reference for setup: https://www.youtube.com/watch?v=GSt00_-0ncQ
# reference for arguments and examples: https://huggingface.co/docs/transformers/en/main_classes/pipelines
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification # Comes from model documentation
import torch
import torch.nn.functional as F

def analyze_sentiment(text_lst,model_name):
    # this function takes several parameters
    # text_lst, this is a series of strings from the dataframe, typically either the lead paragraph or full text

    # Next check if a gpu is available
    device ="cuda:0" if torch.cuda.is_available() else "cpu"

# And set the tokenizer
#tokenizer = 
model_name = "distilbert-base-uncased-finetuned-sst-2-english"

#inputs    = tokenizer(sentence, return_tensors="pt").to(device)
#model     = model.to(device)
#outputs   = model(**inputs)

classifier = pipeline("sentiment-analysis",model=model_name,device=0)
res = classifier("The deposit, in Zambia, could make billions for Silicon Valley, provide minerals for the energy transition and help the United States in its rivalry with China.")
new = classifier("Amazon announced on Wednesday that effectively all of the electricity its operations used last year came from sources that did not produce greenhouse gas emissions. But some experts have criticized the method the company uses to make that determination as being too lenient.")
print(res)
print(new)


#classifier can be given a list, to compute multiple sentiments, returned as an iterable
