from transformers import pipeline 

#sentiment_analysis = pipeline('sentiment-analysis')
#print(sentiment_analysis('I love this'))

class Sentiment:
    def __init__(self, text):
        self.sentiment_analysis = pipeline('sentiment-analysis')
        self.text = text
    def predict(self):
        return self.sentiment_analysis(self.text)[0]['label'], self.sentiment_analysis(self.text)[0]['score']
