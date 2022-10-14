from title2bib.crossref import get_bib_from_title 
from selenium.common.exceptions import NoSuchElementException
import bibtexparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
headers  = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

def get_url(title,scihub = 'https://sci-hub.se'):
    found,bib0 = get_bib_from_title(title,get_first=True)
    # print(bib)
    if found:
        index = bib0.rfind('=')
        index2 = bib0.find('}',index)
        bib1 = bib0[:index2+1]+'\n}'
        bib = bibtexparser.loads(bib1).entries[0]
        # print(bib) 
        if 'doi' in bib:
            url = scihub+'/'+ bib['doi']
            return found,bib['title'],bib['doi'],url,bib
        else:
            return False,bib['title'],None,None,bib
    else:
        return False,None,None,None,{}
    
def download(scihub_url,file,session,web:webdriver):
    
    web.get(scihub_url)
    
    try:
        embed = web.find_element(By.TAG_NAME,'embed')
        url = embed.get_attribute('src')
        print(url)
        f = open(file,'bw')
        re = session.get(url+'.pdf')
        f.write(re.content)
        f.close
        return True
    
    except NoSuchElementException:
        return False