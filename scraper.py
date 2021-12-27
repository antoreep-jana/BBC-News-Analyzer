from bs4 import BeautifulSoup as bs
import requests 
import pandas as pd

from newsparser import BBC
url ='https://www.bbc.com/news/science-environment-56837908'

class ClimateScraper:

	def __init__(self, url:str):
	    article = requests.get(url)
	    self.soup = bs(article.content, "html.parser")
	    self.url = url
	    self.news_links = self.extract_news_links()
		
	def extract_news_links(self) -> list:
	    links = self.soup.find_all('a', {'class' : 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold gs-u-mt+ nw-o-link-split__anchor'})
	    links2 = self.soup.find_all('a', {'class' : "gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"})
	    #print(len(links))
	    #print(len(links2))
	    #for i in links2:
	    #    print(i['href'])
	    result =  [i['href'] for i in links2]
	    result = ['https://www.bbc.com/' + i for i in result if 'https://' not in i]
	    return result
	    
	    
	    
	    
	    
	    
	def extract_data_from_links(self):
	    #df = pd.DataFrame(columns = ['Link', 'Author', 'Date', 'Title', "Body", "Images"])
	    
	    df_links = list()
	    df_authors = list()
	    df_dates = list()
	    df_titles = list()
	    df_body = list()
	    df_images = list()
	    
	    for link in self.news_links:
	        try:
	            parsed = BBC(link)
	            df_links.append(parsed.link)
	            df_authors.append(parsed.author)
	            df_dates.append(parsed.date)
	            df_titles.append(parsed.title)
	            df_body.append(parsed.body)
	            df_images.append(parsed.images)
	            print(parsed.link)
	            print(parsed.author)
	            print(parsed.date)
	            print(parsed.title)
	            print(parsed.body)
	            print(parsed.images)
	            print('--'*10)
	        except:
	            print("Data Invalid")
	    #print(len(df))
	    print(len(df_links))
	    print(len(df_authors))
	    print(len(df_dates))
	    print(len(df_titles))
	    print(len(df_body))
	    print(len(df_images))
	    #df = pd.DataFrame([df_links, df_authors, df_dates, df_titles, df_body, df_images], columns = ['Link', 'Author', 'Date', 'Title', "Body", "Images"])
	    df = pd.DataFrame()
	    df['Link'] = df_links
	    df['Author'] = df_authors 
	    df['Date'] = df_dates 
	    df['Title'] = df_titles 
	    df['Body'] = df_body
	    df['Images'] = df_images
	    df.to_csv('/home/antoreep/Python/Interviews/DeepSearchLabs/data/extracted_data.csv')
		
		
parser = ClimateScraper(url)

print(parser.news_links)
print(parser.extract_data_from_links())
