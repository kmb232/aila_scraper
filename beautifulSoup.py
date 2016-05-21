from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd
import logging
import logging.handlers
 
class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
 
        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.ehlo() # for tls add this line
                smtp.starttls() # for tls add this line
                smtp.ehlo() # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
 
logger = logging.getLogger()
 
gm = TlsSMTPHandler(("smtp.gmail.com", 587), 'kburnett@aila.org', 'Oops', ('kathleenmburnett@gmail.com', '7Pp3anb3FdXa'))
gm.setLevel(logging.ERROR)
 
logger.addHandler(gm)

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

try:
	for i in range(191:197):
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
	logger.exception('Oops.')
	driver.quit()

ina_df.to_csv('ina_links.csv')

driver.quit()