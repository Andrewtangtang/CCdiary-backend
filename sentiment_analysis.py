import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AutoModelForSequenceClassification, AutoTokenizer


class SentimentAnalyser:

    """
    This class is used to analyze the sentiment of a given text.
    INPUT: text (str) - the text to be analyzed
    OUTPUT: probabilities (list) - a list of two lists, where the first list contains the probabilities of the sentiment
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model1 = BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')
        self.model1 = model1.to(self.device)
        self.tokenizer1 = BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')
        model2 = AutoModelForSequenceClassification.from_pretrained("liam168/c2-roberta-base-finetuned-dianping-chinese", num_labels=2)
        self.model2 = model2.to(self.device)
        self.tokenizer2 = AutoTokenizer.from_pretrained("liam168/c2-roberta-base-finetuned-dianping-chinese")

    def analyze_text(self, text):
        encoded_input1 = self.tokenizer1.encode(text, return_tensors="pt").to(self.device)
        output1 = self.model1(encoded_input1)
        probabilities1 = torch.nn.functional.softmax(output1.logits, dim=-1).tolist()
        encoded_input2 = self.tokenizer2.encode(text, return_tensors="pt").to(self.device)
        output2 = self.model2(encoded_input2)
        probabilities2 = torch.nn.functional.softmax(output2.logits, dim=-1).tolist()
        return probabilities1, probabilities2  # lists[0] is for model1, lists[1] is for model2 for the probabilities























