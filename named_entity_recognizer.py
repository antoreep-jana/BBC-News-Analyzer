import spacy
import streamlit as st 
# txt = 'Apple reached an all-time high stock price of 143 dollars this January'

# nlp = spacy.load('en_core_web_trf')
# doc = nlp(txt)

# for ent in doc.ents:
#     print(ent.text)
#     print(ent.label_)
#     print('='*5)

# import gc 
# gc.collect()

## requirements.txt
# https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.2.0/en_core_web_lg-3.2.0.tar.gz#egg=en_core_web_lg
# https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.0.0/en_core_web_trf-3.0.0.tar.gz#egg=en_core_web_trf
    
@st.cache(allow_output_mutation = True, show_spinner = False, max_entries = 6)
def get_model():
    #nlp = spacy.load('en_core_web_trf')
    nlp = spacy.load('en_core_web_lg')
    return nlp

class NER:
    def __init__(self, txt):
        #nlp = spacy.load('en_core_web_sm')
        #nlp = spacy.load('en_core_web_md')
        
        #nlp = spacy.load('en_core_web_lg')
        nlp = get_model()

        #nlp = spacy.load('en_core_web_trf')

        self.entities = []
        self.entityLabels = []

        self.txt = txt 
        self.doc = nlp(txt)

        
    def entRecognizer(self, entDict, typeEnt):
        entList = [ent for ent in entDict if entDict[ent] == typeEnt]
        return entList
        

    def get_entities(self):
        
        for ent in self.doc.ents:
            self.entities.append(ent.text)
            self.entityLabels.append(ent.label_)

        entDict = dict(zip(self.entities, self.entityLabels))

        entOrg = self.entRecognizer(entDict, "ORG")
        entCardinal = self.entRecognizer(entDict, "CARDINAL")
        entPerson = self.entRecognizer(entDict, "PERSON")
        entDate = self.entRecognizer(entDict, "DATE")
        entGPE = self.entRecognizer(entDict, "GPE")

        return entOrg, entCardinal, entPerson, entDate, entGPE