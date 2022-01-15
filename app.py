import streamlit as st 
import spacy
import pandas as pd 
from PIL import Image
import numpy as np 
import torch 
from io import BytesIO
import requests
import re

url ='https://www.bbc.com/news/science-environment-56837908'


st.title('BBC News Scraper')

st.header("Climate Section")

# with st.spinner('Loading and compiling ViT-GPT2 model ...'):

#     from model import *

st.sidebar.markdown("""
A tool to help you analyze the news articles in seconds and deliver you the best insights.
	""")

df = pd.read_csv('data/extracted_data.csv')

cols = st.columns(3)

col1 = cols[0]
data_btn = col1.button("Fetch Latest Data")

col2 = cols[1]

col3 = cols[2]
extracted_data = col3.button("Use the default extracted data")


if extracted_data:
	df = pd.read_csv('data/extracted_data.csv')



if data_btn:
	from scraper import ClimateScraper
	with st.spinner("Fetching latest news articles..."):
		parser = ClimateScraper(url)
		df = parser.extract_data_from_links()



#print(['<select>']+ ['a']))
dates_original = list(df['Date'])
#print(dates_ori)
dates = [i[0:10] for i in dates_original]
date_filter = col2.selectbox("Filter by Date", ['None'] + dates)


if date_filter != "None":
	#print("Here")

	for date in dates_original:
		if date_filter in date:
			df = df[df['Date'] == date]
			#print(df)

mode = st.radio("Mode", ['Simple', 'Advanced'])

if mode == "Simple":

	st.subheader("Please select a news article")

	
	#print(df.Title)
	news_articles = st.selectbox('News Article', list(df.Title))

	#print(df[df['Title'] == news_articles]['Body'][0])
	#print(df[df['Title'] == news_articles]['Body'])

	#print(df.head())
	try:
		#print("here")
		text_lst = df[df['Title'] == news_articles]['Body'][0]
	except:
		#print("except here")
		text_lst = df[df['Title'] == news_articles]['Body']
		text_lst = text_lst.iloc[0]

	
	#print(text_lst.iloc[0])
	#print(type(text_lst))
	text = ""
	for txt in text_lst:
		text += txt 

	text = text.replace("[", "").replace("]", "").replace("'",'')
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
		with st.spinner("Calculating Sentiment..."):
			sentiment = Sentiment(text)

			st.write("Sentiment :" ,  sentiment.predict()[0])
			st.write("Confidence :",  sentiment.predict()[1])


		#sents = sent_tokenize(text)
		#entireText = TextBlob(text)
		

	elif option == "Entity Extraction":

		#text_ent = "This is an Apple watch. Costed about $100 on 21st June, 2022."
				

		from named_entity_recognizer import NER 

		ents = NER(text)

		entOrg, entCardinal, entPerson, entDate, entGPE = ents.get_entities()

		filter_ent = st.selectbox("Choose entity type : ", ['Organization Entities', 'Cardinal Entities', 'Personal Entities', 'Date Entities', 'GPE Entities'])

		#print(text)
		if filter_ent == "Organization Entities":
			#st.write("Organization Entities : " + str(entOrg))
			selection = st.radio("Organization Entities", entOrg)
	
		elif filter_ent == "Cardinal Entities":
			#st.write("Cardinal Entities : " + str(entCardinal))
			selection = st.radio("Cardinal Entities", entCardinal)
		elif filter_ent == "Personal Entities":
			#st.write("Personal Entities : " + str(entPerson))
			selection = st.radio("Personal Entities", entPerson)
		elif filter_ent == "Date Entities":
			#st.write("Date Entities : " + str(entDate))
			selection = st.radio("Date Entities", entDate)
		elif filter_ent == "GPE Entities":
			#st.write("GPE Entities: " + str(entGPE))
			selection = st.radio("GPE Entities", entGPE)
		#st.write('Excerpts quoting"', selection, '" coming soon' )

		excerpt = re.findall(r"([^.]*?" + re.escape(selection) + r"[^.]*\.)", text)

		excerpt = "".join(excerpt)
		#print(excerpt)

		#st.markdown("####Excerpts quoting ", selection)
		st.markdown(excerpt.replace(selection, "**" + selection + "**"))

	elif option == "Image Analysis":

		st.write("Under Making!")

		from image_captioner import ImageCaption

		#df = pd.read_csv('data/extracted_data.csv')
		imgs = df[df['Title'] == news_articles]['Images']
		#print(list(imgs)[0])

		bad_img_urls = ['https://ichef.bbci.co.uk/news/976/cpsprodpb/1848/production/_98761260_onlinebanner_976x280.jpg', 'https://ichef.bbci.co.uk/news/2048/cpsprodpb/155C6/production/_120449478_bottom-3x.png', 'https://ichef.bbci.co.uk/news/2048/cpsprodpb/163F9/production/_120892119_summit_top-3x-002.png', 'https://ichef.bbci.co.uk/news/2048/cpsprodpb/102F3/production/_121319266_indonesia_v2-nc.png', 'https://ichef.bbci.co.uk/news/464/cpsprodpb/16C07/production/_87719139_line976.jpg']
		imgs = list(imgs)[0].replace("[", "").replace("]", "").replace("'","").split(", ")

		imgs = [i for i in imgs if i not in bad_img_urls]		
		#print(imgs)
		with st.spinner("Generating image caption..."):

			st.write("Better Graph in upcoming versions!")

			image = Image.open('data/img.jpg')
			

			#ncols = len(imgs)
			#cols = st.columns(ncols)
			#print(ncols)
			
			#for i in range(ncols):
				
			#	try:
			#		col = cols[i]
			#		response = requests.get(imgs[i])
			#		img = Image.open(BytesIO(response.content))
			#		col.image(img)
			#	except:
			#		pass
				#col.image(image)


			#print(len(imgs.tolist()))
			

			text_image_radio = st.radio('Text Generator', ['Alt text', "Image Caption Model"])
			
			if text_image_radio == 'Alt text':
				caption = 'This is Alt Text caption. The one provided in the BBC articles.'
				captions = ['caption_' + str(i + 1) for i in range(len(imgs))]
			
			else:
				#print(imgs)
				st.write("Generated Captions using dummy image caption model. Attention-based caption model coming soon!")

				captions = list()
					
				for i in imgs:
					captioner = ImageCaption(i)
					caption = captioner.predict()
					#print(caption)
					#print(captions)
					captions.append(caption)

			#print(captions)
			st.image(imgs,caption = captions, use_column_width = True)
			

			#st.image(image, caption = caption)
				
			
			#st.write(caption)

	elif option == "Knowledge Graph":

		with st.spinner("Generating Knowledge Graph..."):

			#st.graphviz_chart('digraph  {\n"External COVID-19 links";\n"Idaho Coronavirus Twitter";\nMontana;\n"External United links";\n"South Dakota Health";\nUtah;\n"West Virginia Health";\nWyoming;\n"External COVID-19 links" -> "Idaho Coronavirus Twitter"  [edge="Information from", key=0];\n"External COVID-19 links" -> Montana  [edge="Information from", key=0];\n"External COVID-19 links" -> Utah  [edge="Information from", key=0];\n"External COVID-19 links" -> "West Virginia Health"  [edge="Information from", key=0];\n"External COVID-19 links" -> Wyoming  [edge="Information from", key=0];\n"External United links" -> "South Dakota Health"  [edge="Information from", key=0];\n}\n')
			from knowledge_graph import KnowledgeGraph 


			graph = KnowledgeGraph(text)
			graph.generate_graph()
			st.image("tmp/knowledge_graph.jpg")

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
		with st.spinner("Generating summary..."):
			summary = Summarizer(text)
			#summWords = "This is the abstract!"
			st.subheader("Summary")
			st.write(summary.summarize().replace("<pad>", "").replace("</s>","").replace("<extra_id_0>", ""))
	st.text("")
	st.text("")
	st.download_button("Download Analysis Report!", data = 'data/sample_analysis_report.pdf', file_name = 'sample_analysis_report.pdf', mime = 'application/octet-stream')
else:

	st.write("Advanced Section Under Making!")

st.markdown("***")
st.write("**Developer**: Antoreep Jana")
st.write("**Mail**: antoreepjana@gmail.com")
st.write("Code at my GitHub repo [BBC News Analyzer](https://github.com/antoreep-jana/BBC-News-Analyzer.git)")