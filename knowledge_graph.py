"""import spacy

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


doc = nlp("The drawdown process is governed by astm standard d823")

for tok in doc:
	print(tok.text, "...", tok.dep_)


candidate_sentences = pd.read_csv("data/wiki_sentences_v2.csv")

def get_entities(sent):
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  #############################################################
  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text
  #############################################################

  return [ent1.strip(), ent2.strip()]

entity_pairs = []

for i in tqdm(candidate_sentences["sentence"]):
  entity_pairs.append(get_entities(i))

 

def get_relation(sent):

  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1", [pattern], on_match = None) 

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text)

relations = [get_relation(i) for i in tqdm(candidate_sentences['sentence'])]

# extract subject
source = [i[0] for i in entity_pairs]

# extract object
target = [i[1] for i in entity_pairs]

kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})


G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="composed by"], "source", "target", 
                          edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(12,12))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
plt.show()"""


import spacy
import networkx as ntx
from spacy.matcher import Matcher
import pandas as pd
import matplotlib.pyplot as plot
import nltk

import streamlit as st 

# import gc 
# gc.collect()

@st.cache(allow_output_mutation = True, show_spinner = False, max_entries = 4)
def get_model():
	nlp = spacy.load('en_core_web_lg')
	#nlp = spacy.load("en_core_web_trf")
	return nlp

class KnowledgeGraph:

	def __init__(self, text):

		self.text = text 

		self.sentences = self.convert_to_sentences(self.text)
		#self.nlp = spacy.load('en_core_web_lg')
		self.nlp = get_model()


	def convert_to_sentences(self, text):
		nltk.download('punkt')

		return nltk.tokenize.sent_tokenize(text)


	def obtain_relation(self, sent):

		doc = self.nlp(sent)

		matcher = Matcher(self.nlp.vocab)

		pattern = [{"DEP" : "ROOT"},
				{"DEP" : "prep", "OP" : "?"},

				{"DEP" : "agent", "OP" : "?"},
				{"POS" : "ADJ", "OP" : "?"}
		]

		matcher.add("matching_1", [pattern], on_match = None)

		matcher = matcher(doc)
		h = len(matcher)  - 1
		span = doc[matcher[h][1]: matcher[h][2]]

		return span.text


	def extract_entities(self, sents):

		enti_one = ""

		enti_two = ""

		dep_prev_token = ""

		txt_prev_token = ""

		prefix = ""

		modifier = ""


		for tokn in self.nlp(sents):

			if tokn.dep_ != "punct":

				if tokn.dep_ == "compound":

					prefix = tokn.text 

					if dep_prev_token == "compound":

						prefix = txt_prev_token + " " + tokn.text 

				if tokn.dep_.endswith("mod") == True:

					modifier = tokn.text 

					if dep_prev_token == "compound":

						modifier = txt_prev_token + " " + tokn.text 

				if tokn.dep_.find("subj") == True:

					enti_one = modifier + " " + prefix + " " + tokn.text 

					prefix = ""
					modifier = ""
					dep_prev_token = ""
					txt_prev_token = ""

				if tokn.dep_.find("obj") == True:

					enti_two = modifier + ' ' + prefix + " " + tokn.text 


				dep_prev_token = tokn.dep_  
				txt_prev_token = tokn.text  

		return [enti_one.strip(), enti_two.strip()]



	def generate_graph(self):

		
		pairs_of_entities = []
		#pairs_of_entities.append(self.extract_entities(self.text))
		for i in self.sentences:

			pairs_of_entities.append(self.extract_entities(i))
		#print(pairs_of_entities)

		#relations = [self.obtain_relation(j) for j in tqdm(data['text'][:800])]
		relations = [self.obtain_relation(j) for j in self.sentences]

		#print(relations)

		# subject extraction
		source = [j[0] for j in pairs_of_entities]

		#object extraction
		target = [k[1] for k in pairs_of_entities]

		data_kgf = pd.DataFrame({'source':source, 'target':target, 'edge':relations})

		#print(data_kgf)
		graph = ntx.convert_matrix.from_pandas_edgelist(data_kgf, "source", "target",
                         edge_attr=True, create_using=ntx.MultiDiGraph())

		#print(graph.edges())
		
		plot.figure(figsize=(14,14))
		#print("Graph", graph)
		pos = ntx.spring_layout(graph, k = 0.5) # k regulates the distance between nodes
		ntx.draw(graph, with_labels=True, node_color='green', node_size=1400, edge_cmap=plot.cm.Blues, pos = pos)

		plot.savefig("tmp/knowledge_graph.jpg")

		#return "tmp/knowledge_graph.png"