# from selenium import webdriver
# from time import sleep 

# url = 'https://www.bbc.co.uk/news/science-environment-56837908'


# from selenium.webdriver.chrome.service import Service


# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# #options.add_argument("--kiosk")
# options.add_argument("no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--incognito")
# #options.add_argument("--window-size=1920x1080")
# ##options.add_argument("--start-fullscreen")


# ser = Service("./driver/chromedriver")
# driver = webdriver.Chrome(service = ser, options = options)
# #driver.maximize_window()

# driver.get(url)
# sleep(10)
# xbutton = driver.find_element_by_xpath('//*[@id="responsive-news"]/body/div[9]/div/button')
# xbutton.click() 

# #news_links = driver.find_elements_by_xpath('//*[@id="topos-component"]/div[3]/div[2]/div[1]/#div/div/div/div[1]/div/div[2]/div[1]/a')

# #news_links = driver.find_elements_by_class_name('gel-layout__item gel-1/3@m gel-1/4@l gel-1/5@xxl nw-o-keyline nw-o-no-keyline@m')


# news_links = driver.find_elements_by_css_selector('div.gel-1\/1\@xxl:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
# """
# class = gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor

# gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor

# XPath = //*[@id="topos-component"]/div[3]/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div[1]/a

# //*[@id="topos-component"]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div/div[2]/div[1]/a
# """
# for elem in news_links:
# 	print(elem.get_attribute('href'))
# #driver.quit()


