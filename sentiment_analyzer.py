from transformers import pipeline 
from transformers import BertForSequenceClassification, BertTokenizer
import torch
#sentiment_analysis = pipeline('sentiment-analysis')
#print(sentiment_analysis('I love this'))

# exceeds 1024 throws error 

# chuck the data into part


class Sentiment:
    def __init__(self, text):
        #self.sentiment_analysis = pipeline('sentiment-analysis', model = 'siebert/sentiment-roberta-large-english')
        self.text = text
        #self.text = "This is very very bad"*200
        #self.tokenizer = BertTokenizer.from_pretrained('siebert/sentiment-roberta-large-english')
        #self.model = BertForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
        self.tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
        self.model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')
        self.tokens = self.tokenizer.encode_plus(self.text, add_special_tokens = False, return_tensors = 'pt')


        



    def predict(self):

        chunksize = 512


        input_id_chunks = self.tokens['input_ids'][0].split(510)
        mask_chunks = self.tokens['attention_mask'][0].split(510)

        input_id_chunks = list(input_id_chunks)
        mask_chunks = list(mask_chunks)

        for i in range(len(input_id_chunks)):
            input_id_chunks[i] = torch.cat([torch.Tensor([101]), input_id_chunks[i], torch.Tensor([102])])

            mask_chunks[i] = torch.cat([
                torch.Tensor([1]), mask_chunks[i], torch.Tensor([1])
                ])

            pad_len = chunksize - input_id_chunks[i].shape[0]

            if pad_len > 0:

                input_id_chunks[i] = torch.cat([
                        input_id_chunks[i], torch.Tensor([0] * pad_len)
                    ])

                mask_chunks[i] = torch.cat([
                        mask_chunks[i], torch.Tensor([0] * pad_len)
                    ])

        input_ids = torch.stack(input_id_chunks)

        attention_mask = torch.stack(mask_chunks)

        input_dict = {
        "input_ids" : input_ids.long(),
        "attention_mask" : attention_mask.int()

        }

        outputs = self.model(**input_dict)

        probs = torch.nn.functional.softmax(outputs[0], dim = -1)
        mean = probs.mean(dim = 0)


        senti = torch.argmax(mean).item()
        if senti == 1:
            return 'Positive', round(mean[senti].item(), 3)
        elif senti == 0:
            return 'Negative', round(mean[senti].item(), 3)
        else:
            return "Neutral", round(mean[senti].item(), 3)

        #return self.sentiment_analysis(self.text)[0]['label'], self.sentiment_analysis(self.text)[0]['score']
