import streamlit as st 
import spacy
import pandas as pd 
from PIL import Image

st.title('BBC News Scraper')

st.header("Climate Section")

# with st.spinner('Loading and compiling ViT-GPT2 model ...'):

#     from model import *

st.sidebar.markdown("""
A tool to help you analyze the news articles in seconds and deliver you the best insights.
	""")

data_btn = st.button("Fetch Latest Data")

if data_btn:
	pass

mode = st.radio("Mode", ['Simple', 'Advanced'])

if mode == "Simple":

	st.subheader("Please select a news article")

	df = pd.read_csv('data/extracted_data.csv')
	#print(df.Title)
	news_articles = st.selectbox('News Article', list(df.Title))

	#print(df[df['Title'] == news_articles]['Body'][0])
	#print(df[df['Title'] == news_articles]['Body'])
	text_lst = df[df['Title'] == news_articles]['Body']
	text = ""
	for txt in text_lst:
		text += txt 

	st.subheader("Select Operation")
	option = st.selectbox('NLP Service', ('Sentiment Analysis', 'Entity Extraction', 'Text Summarization', 'Knowledge Graph', 'Image Analysis'))


	#st.subheader("Enter the text you'd like to analyze")


	#text = st.text_input("Enter Text")

	st.header('Results')

	#sentiment = "Positive"
	#st.write(sentiment)

	#st.write("BBC News Articles APP")

	# def entRecognizer(entDict, typeEnt):

	# 	entList = [ent for ent in entDict if entDict[ent] == typeEnt]
	# 	return entList

	if option == "Sentiment Analysis":
		from sentiment_analyzer import Sentiment

		#text = "This is an Apple watch. Great Investment. Costed about $100 on 21st June, 2022."

		sentiment = Sentiment(text)

		st.write("Sentiment :" ,  sentiment.predict()[0])
		st.write("Confidence :",  sentiment.predict()[1])


		#sents = sent_tokenize(text)
		#entireText = TextBlob(text)
		

	elif option == "Entity Extraction":

		#text = "This is an Apple watch. Costed about $100 on 21st June, 2022."
		text = """
		This sentence has 10 words and we are testing it.
		"""*30		

		from named_entity_recognizer import NER 

		ents = NER(text)

		entOrg, entCardinal, entPerson, entDate, entGPE = ents.get_entities()

		filter_ent = st.selectbox("Choose entity type : ", ['Organization Entities', 'Cardinal Entities', 'Personal Entities', 'Date Entities', 'GPE Entities'])

		if filter_ent == "Organization Entities":
			st.write("Organization Entities : " + str(entOrg))
		elif filter_ent == "Cardinal Entities":
			st.write("Cardinal Entities : " + str(entCardinal))
		elif filter_ent == "Personal Entities":
			st.write("Personal Entities : " + str(entPerson))
		elif filter_ent == "Date Entities":
			st.write("Date Entities : " + str(entDate))
		elif filter_ent == "GPE Entities":
			st.write("GPE Entities: " + str(entGPE))

	elif option == "Image Analysis":

		st.write("Under Making!")

		with st.spinner("Generating image caption..."):

			image = Image.open('data/How-to-Develop-a-Deep-Learning-Caption-Generation-Model-in-Python-from-Scratch.jpg')
			
			text_image_radio = st.radio('Text Generator', ['Alt text', "Image Caption Model"])
			
			if text_image_radio == 'Alt text':
				caption = 'This is Alt Text caption. The one provided in the BBC articles.'
			else:
				caption = "There are two dogs roaming the deserts."

			st.image(image, caption = caption)
				
			
			#st.write(caption)

	elif option == "Knowledge Graph":

		st.write("Under Making!")

	else:

		#summWords = summarize(text)

		from summarizer import Summarizer 
	# 	text = 
	# New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York. A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband. Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
	# In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
	# Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
	# 2010 marriage license application, according to court documents.
	# Prosecutors said the marriages were part of an immigration scam.
	# On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
	# After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
	# Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
	# All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
	# Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
	# Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
	# The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
	# Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
	# Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
	# If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
		
		summary = Summarizer(text)
		#summWords = "This is the abstract!"
		st.subheader("Summary")
		st.write(summary.summarize())
	st.text("")
	st.text("")
	st.download_button("Download Analysis Report!", data = 'data/sample_analysis_report.pdf', file_name = 'sample_analysis_report.pdf', mime = 'application/octet-stream')
else:

	st.write("Advanced Section Under Making!")

st.markdown("***")
st.write("**Developer**: Antoreep Jana")
st.write("**Mail**: antoreepjana@gmail.com")
st.write("Code at my GitHub repo [BBC News Analyzer](https://github.com/antoreep-jana/BBC-News-Analyzer.git)")