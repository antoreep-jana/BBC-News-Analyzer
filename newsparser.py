from bs4 import BeautifulSoup as bs
import requests 

class BBC:
    def __init__(self, url:str):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        #print(dir(self.soup))
        #print(self.soup.h1.text)
        self.body = self.get_body()
        self.link = url
        self.title = self.get_title()
        self.author = self.get_author()
        self.images = self.get_images()
        self.date = self.get_date()
        #author = self.soup.find
        
        
        
        #date = self.soup
        
        #for img in imgs:
        #	print(img['src'])
        
        
        paras = self.soup.find_all('div', {"class" : "ssrcss-17j9f6r-RichTextContainer e5tfeyi1"})
        #for para in paras:
        #	print(para.text)
        
    def get_body(self) -> list:
        #body = self.soup.find(property="articleBody")
        
        paras = self.soup.find_all('div', {"class" : "ssrcss-17j9f6r-RichTextContainer e5tfeyi1"})
        
        #for para in paras:
        #	print(para.text)
        return [p.text for p in paras]
        #return [p.text for p in body.find_all("p")]
    
    def get_title(self) -> str:
        #return self.soup.find(class_="story-body__h1").text
        return self.soup.h1.text
        
    def get_author(self) -> str:
    	author = self.soup.find('p', {'class' : 'ssrcss-1rv0moy-Contributor e5xb54n2'})
    	return author.text.replace("BBC News", "")
    	
    def get_images(self) -> list:
        imgs = self.soup.find_all('figure', {'class' : 'ssrcss-wpgbih-StyledFigure e34k3c23'})
    	
        imgs_lst = []
        
        for img in imgs:
        	try:
        		if "blank_white_space" not in img.img['src']:
        			imgs_lst.append(img.img['src'])#['div']['span']['span']['img'])
        	except:
        		pass
         		
        return imgs_lst
        
    def get_date(self) -> str:
    	date = self.soup.find_all('time')[0]
    	return date['datetime']
		
parsed = BBC("https://www.bbc.co.uk/news/world-europe-49345912") 

#print(parsed.title)
print(parsed.link)
print(parsed.author)
print(parsed.date)
print(parsed.title)
print(parsed.body)
print(parsed.images)
#print(parsed.body)
		

