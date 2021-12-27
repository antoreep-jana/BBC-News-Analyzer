import spacy

#nlp = spacy.load('en_core_web_trf')

#doc = nlp("The 22-year-old recently won ATP Challenger tournament.")

#for tok in doc:
#	print(tok.text, "...", tok.dep_)


import re 
import pandas as pd 
import bs4 
import requests 
import spacy 
from spacy import displacy 

nlp = spacy.load('en_core_web_trf')


from spacy.matcher import Matcher
from spacy.tokens import Span 

import networkx as nx 

import matplotlib.pyplot as plt 
from tqdm import tqdm 


pd.set_option('display.max_colwidth', 200)


candidate_sentences = pd.read_csv('data/wiki_sentences_v2.csv')

