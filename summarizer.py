from transformers import pipeline 


class Summarizer:

	def __init__(self, text):

		self.text = text

		self.summarizer = pipeline('summarization') 

	def summarize(self):

		return self.summarizer(self.text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']