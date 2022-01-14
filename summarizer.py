from transformers import pipeline 

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  
import streamlit as st 


# import gc 
# gc.collect()


@st.cache(allow_output_mutation = True, show_spinner = False, max_entries = 6)
def get_models():
	#model = AutoModelForSeq2SeqLM.from_pretrained('t5-base')
	model = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-base')
	#tokenizer = AutoTokenizer.from_pretrained('t5-base')
	tokenizer = AutoTokenizer.from_pretrained('facebook/bart-base')
	return model, tokenizer

class Summarizer:

	def __init__(self, text):

		self.text = text

		#self.summarizer = pipeline('summarization') 

		#self.model = AutoModelForSeq2SeqLM.from_pretrained('t5-base')
		#self.tokenizer = AutoTokenizer.from_pretrained('t5-base')

		self.model, self.tokenizer = get_models()

		self.inputs = self.tokenizer(self.text, return_tensors = 'pt', max_length = 512, truncation = True)



	def summarize(self):

		#return self.summarizer(self.text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']	
		outputs = self.model.generate(self.inputs['input_ids'], max_length = 250, min_length = 40, length_penalty = 2.0, num_beams = 4, early_stopping = True)
		#print(outputs)
		return self.tokenizer.decode(outputs[0])