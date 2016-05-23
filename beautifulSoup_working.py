from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd
import logging
import logging.handlers
 

fp = webdriver.FirefoxProfile('C:\\Users\\Kathleen\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\cfc3dns7.default')
driver = webdriver.Firefox(firefox_profile=fp)


#INA
#Returns dataframe that will be addded to the master DataFrame
def ina_links(soup, url):
	link_df = pd.DataFrame(columns=['Citation','Link'])
	paras = soup.find_all("p")
	for para in paras:
		if para.find(class_="INACitation") == None:
			citation = next(span.string for span in soup.find("span",class_="INACitation") for h1 in soup.find('h1'))
			if citation != None:
				linkcite = "INA §" + citation
				linkurl = "/#documents/" + str(url)
				page_df=pd.DataFrame({'Citation': linkcite, 'Link': linkurl}, index=[0])
				frames = [page_df,link_df]
				link_df = pd.concat(frames)
			else: 
				pass
		else:
			citation = para.find(class_="INACitation")
			specific_citation = citation.string
			linkcite = "INA §" + specific_citation
			link = para.find_next_sibling("a")
			jump = link.get('name')
			linkurl = str(url) + "#" + jump
			page_df=pd.DataFrame({'Citation': linkcite, 'Link': linkurl}, index=[0])
			frames = [page_df,link_df]
			link_df = pd.concat(frames)
	return link_df

#Create Master Dataframes
ina_df = pd.DataFrame(columns=['Citation','Link'])


for i in range(10,300):
	try:
		url = "http://ailalink.aila.org/#documents/" + str(i)
		driver.get(url)
		time.sleep(1)
		content = driver.find_element_by_id("content")
		html = content.get_attribute('innerHTML')
		soup = BeautifulSoup(html, "html.parser")
		breadcrumb = soup.find(id="document-content-bar")
		if breadcrumb.find("a", string="INA") != None:
			ina_page = ina_links(soup,i)
			frames=[ina_df,ina_page]
			ina_df = pd.concat(frames)
		else:
			pass
	except:
		pass
		

ina_df.to_csv('ina_links.csv')

driver.quit()