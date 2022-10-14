
import os
import xml.dom.minidom
import numpy as np
import pandas as pd
from .my_scihub import get_url,download
from selenium import webdriver
from requests import session

proxies={
    'http':'127.0.0.1:1087',
    'https':'127.0.0.1:1087'
}
   
def excel_post(xls_f,proxy=None):
   option = webdriver.ChromeOptions()
   if proxy != None:
      option.add_argument('--proxy-server=%s'%proxy)
   web = webdriver.Chrome()
   first = web.get('https://sci-hub.se')
   proxies={
      'http':'127.0.0.1:1087',
      'https':'127.0.0.1:1087'
   }
   
   def get_cookie(cookie):
      '''cookie from selenium
      '''
      cookie1 = [cookie[0]['name'],cookie[0]['value']]
      cookie2 = [cookie[1]['name'],cookie[1]['value']]

      return f'{cookie1[0]}={cookie1[1]};{cookie2[0]}={cookie2[1]}'
   headers  = {
      'cookies':get_cookie(web.get_cookies()),
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
   }
   sec = session()
   sec.headers = headers
   # sec.proxies = proxies
   
   
   table = pd.read_excel(xls_f)
   dir = xls_f[:-5]
   if not os.path.exists(dir):
      os.makedirs(dir)
   if not os.path.exists(dir+'/pdf'):
      os.makedirs(dir+'/pdf')
      
   md = open(dir+f"/{dir}.md",'w')
   md.write(f"# {dir}\n")
   md.close()
   for id,title in enumerate(table['title'],0):
      md = open(dir+f"/{dir}.md",'a')
      if title.find('\xa0')!=-1:
         title = title[:title.find('\xa0')]
      print(id,title)
      md.write(f'## {title}\n')
      link = table['link'][id]
      snippet = table['snippet'][id]
      try:
         found,tit,doi,url,bib = get_url(title)
      except Exception:
         found,tit,doi,url,bib = False,None,None,None,{}
      if 'year' in bib:
         year = bib['year']
         md.write(f'- year\n\t- {year}\n')
      else:
         md.write(f'- year\n\t- Unknown\n')
         
      md.write(f'- link\n\t- {link}\n')
      md.write(f'- snippet\n\t- {snippet}\n')
      md.write(f'- get\n')
      
      f_title = title.replace(' ','_').replace('\xa0','').replace('/','|')
      print(found,tit,doi,url,f_title)
      down = False
      if found:
        down = download(url,os.path.abspath('%s/pdf/%s.pdf'%(dir,f_title)),session=sec,web=web)

      md.write(f'\t- found: {found}\n')
      if down:
         md.write('\t- title: [%s](./pdf/%s.pdf)\n'%(tit,f_title))
      else:
         md.write('\t- title: %s\n'%(tit))
      md.write(f'\t- doi: {doi}\n')
      
      md.close()
      
      
# def post(xml_f):
#    excel_post(xml_f[:-5]+'.xlsx')

