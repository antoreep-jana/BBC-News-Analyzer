import spacy
import streamlit as st 
# txt = 'Apple reached an all-time high stock price of 143 dollars this January'

# nlp = spacy.load('en_core_web_trf')
# doc = nlp(txt)

# for ent in doc.ents:
#     print(ent.text)
#     print(ent.label_)
#     print('='*5)
    
@st.cache(allow_output_mutation = True)
def get_model():
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