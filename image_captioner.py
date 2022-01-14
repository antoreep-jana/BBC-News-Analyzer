import numpy as np 
#import tensorflow as tf    
import requests
from tqdm import tqdm
#from tensorflow.keras.preprocessing.text import Tokenizer   
#from tensorflow.keras.preprocessing.sequence import pad_sequences
import os 
import subprocess
import urllib3
import torch
from torchvision import transforms

from PIL import Image

from time import sleep

from image_captioning_model import load_model, generate_caption
import streamlit as st 

## NEXT UP -> https://github.com/rmokady/CLIP_prefix_caption

@st.cache
def get_vocabs():

	#vocab file 
	vocab_file = "https://www.dl.dropboxusercontent.com/s/7x49kzzva29z2bt/vocab.pkl?dl=0"
		
	#r = requests.get(vocab_file, allow_redirects = True)
	#open('data/vocab.pkl').write(r.content)
		
	if not os.path.isfile('data/vocab.pkl'):		
		download(vocab_file, 'data/vocab.pkl')

@st.cache
def download(url, file_name):
	get_response = requests.get(url,stream=True)
	with open(file_name, 'wb') as f:
		for chunk in get_response.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)

@st.cache
def get_models():

	## download models 
	#decoder model 


	url_decoder = 'https://www.dl.dropboxusercontent.com/s/fnc7qg6snrusbp2/decoder-5-3000.pkl?dl=0'
	#decoder_file = urllib3.urlopen(url_decoder)
	#with open('models/decoder-5-3000.pkl') as output:
	#	output.write(decoder_file.read())
		

	if not os.path.isfile('models/decoder-5-3000.pkl'):
		download(url_decoder, 'models/decoder-5-3000.pkl')
	#r = requests.get(url_decoder, allow_redirects = True)
	#open('models/decoder-5-3000.pkl').write(r.content)

	#encoder model
	url_encoder = "https://www.dl.dropboxusercontent.com/s/g8t2oaxiincu48w/encoder-5-3000.pkl?dl=0"
	#r = requests.get(url_encoder, allow_redirects = True)
	#open('models/encoder-5-3000.pkl').write(r.content)
		
	if not os.path.isfile('models/encoder-5-3000.pkl'):
		download(url_encoder, 'models/encoder-5-3000.pkl')


class ImageCaption:

	def __init__(self, img):

		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		#download the models data
		get_models()

		#download the vocab file
		get_vocabs()

		self.img = img 

		self.img_file = self.read_img_url(self.img)




	def read_img_url(self, img_url):

		image = Image.open(requests.get(img_url, stream = True).raw).convert("RGB")

		img_name = img_url.split("/")[-1]
		image.save("tmp/" + img_name)
		return "tmp/" + img_name
	
	def predict(self):


		#from image_captioning.sample import predict_main 
		#return "A sentence"
		#return predict_main(self.img)

		
		encoder, decoder, vocab, transform = load_model()
		return generate_caption(self.img_file, encoder, decoder, vocab, transform )

		#sleep(3)

		#output = subprocess.Popen(["python","sample.py","--image", self.img_file], stdout = subprocess.PIPE)

		#print(output)

		#os.system('python sample.py --image data/img.jpg')
		
		#return output.communicate()[0].decode('utf-8').replace('<start>', "").replace('<end>', '')
		

		#return "Image Captioning model in progress"
