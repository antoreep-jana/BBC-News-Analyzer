import numpy as np 
#import tensorflow as tf    
import requests
from tqdm import tqdm
#from tensorflow.keras.preprocessing.text import Tokenizer   
#from tensorflow.keras.preprocessing.sequence import pad_sequences
import os 
import subprocess
import urllib3
from torchvision import transforms

class Sampler:

	def __init__(self):

		pass 

	def load_img(self):
		pass 


class VocabBuilder:
	def __init__(self):

		pass 

class Model:

	def __init__(self):

		pass 

class Resize:

	def __init__(self):

		pass 


class ImageCaption:

	def __init__(self, img):

		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		#download the models data
		self.get_models()

		#download the vocab file
		self.get_vocabs()

		self.img = img 

	def download(self, url, file_name):
		get_response = requests.get(url,stream=True)
		with open(file_name, 'wb') as f:
			for chunk in get_response.iter_content(chunk_size=1024):
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)


	def get_vocabs(self):

		#vocab file 
		vocab_file = "https://www.dl.dropboxusercontent.com/s/7x49kzzva29z2bt/vocab.pkl?dl=0"
		
		#r = requests.get(vocab_file, allow_redirects = True)
		#open('image_captioning/data/vocab.pkl').write(r.content)
		
		if not os.path.isfile('image_captioning/data/vocab.pkl'):		
			self.download(vocab_file, 'image_captioning/data/vocab.pkl')

	def get_models(self):

		## download models 
		#decoder model 


		url_decoder = 'https://www.dl.dropboxusercontent.com/s/fnc7qg6snrusbp2/decoder-5-3000.pkl?dl=0'
		#decoder_file = urllib3.urlopen(url_decoder)
		#with open('image_captioning/models/decoder-5-3000.pkl') as output:
		#	output.write(decoder_file.read())
		

		if not os.path.isfile('image_captioning/models/decoder-5-3000.pkl'):
			self.download(url_decoder, 'image_captioning/models/decoder-5-3000.pkl')

		#r = requests.get(url_decoder, allow_redirects = True)
		#open('image_captioning/models/decoder-5-3000.pkl').write(r.content)

		#encoder model
		url_encoder = "https://www.dl.dropboxusercontent.com/s/g8t2oaxiincu48w/encoder-5-3000.pkl?dl=0"
		#r = requests.get(url_encoder, allow_redirects = True)
		#open('image_captioning/models/encoder-5-3000.pkl').write(r.content)
		
		if not os.path.isfile('image_captioning/models/encoder-5-3000.pkl'):
			self.download(url_encoder, 'image_captioning/models/encoder-5-3000.pkl')


	def predict(self):


		#from image_captioning.sample import predict_main 
		#return "A sentence"
		#return predict_main(self.img)

		#output = subprocess.Popen(["python","image_captioning/sample.py","--image", "data/img.jpg"], stdout = subprocess.PIPE)

		#os.system('python image_captioning/sample.py --image data/img.jpg')
		#return output.communicate()[0].decode('utf-8').replace('<start>', "").replace('<end>', '')
		return "Image Captioning model in progress"
