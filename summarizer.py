from transformers import pipeline 

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  
class Summarizer:

	def __init__(self, text):

		self.text = text

		#self.summarizer = pipeline('summarization') 

		self.model = AutoModelForSeq2SeqLM.from_pretrained('t5-base')
		self.tokenizer = AutoTokenizer.from_pretrained('t5-base')

		self.inputs = self.tokenizer(self.text, return_tensors = 'pt', max_length = 512, truncation = True)



	def summarize(self):

		#return self.summarizer(self.text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']	
		outputs = self.model.generate(self.inputs['input_ids'], max_length = 150, min_length = 40, length_penalty = 2.0, num_beams = 4, early_stopping = True)
		#print(outputs)
		return self.tokenizer.decode(outputs[0])