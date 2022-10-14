from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException


def find_element(webdrive,by,value):
    try:
        return webdrive.find_element(by=by,value=value)
    except NoSuchElementException:
        return None

class crawl():
    def __init__(self,web,key_word:str,proxy,year=None,sort = 'relevance',number = None) -> None:
        # print('init')
        self.res = []
        self.index = ['title','link','snippet']
        self.year = year
        self.keyword = key_word
        option = webdriver.ChromeOptions()
        if proxy!= None:
            option.add_argument('--proxy-server=%s'%proxy)
        self.web = webdriver.Chrome(options=option)
        # self.position = 0
        self.end = False
        s = 0
        if sort =='date':
            s = 1
        elif sort=='date_everything':
            s= 2
        self.tree = dict(
            year = f'&as_ylo={year:d}' if self.year!=None else '',
            sort = '&scisbd=%d'%s
            
        )
        # print(self.tree)
        self.url = web+'/scholar?'+'q='+self.keyword.replace(' ','+')+self.tree['year']+self.tree['sort']
        print(self.url)
        self.web.get(self.url)
        _bot = find_element(self.web,by=By.XPATH,value='//form[@id="captcha-form"]')
        if _bot==None:
            time.sleep(100)
            _bot = find_element(self.web,by=By.XPATH,value='//form[@id="captcha-form"]')
        
        self.web.get(self.url)
        
        res_info = self.web.find_element(by=By.XPATH,value='//div[@id="gs_ab_md"]/div[@class="gs_ab_mdw"]')
        self.res_num = int(res_info.text.split(' ')[1].replace(',',''))
        self.number = self.res_num if number==None else min([number,self.res_num])
        
        
        
    def get(self,position=0):
        print(self.url+'&start=%d'%position)
        self.web.get(self.url+'&start=%d'%position)
        res = self.web.find_elements(by=By.XPATH,value='//*[@data-rp]')
        for r in res:
            div = r.find_element(by=By.XPATH,value='.//h3')
            _type = find_element(div,By.XPATH,value='.//span')
            remove = _type.text if _type != None else ''
            _link = find_element(div,by=By.XPATH,value='.//a[@href]')
            link = _link.get_attribute('href') if _link != None else ''
            title = div.text.replace(remove,'').strip()
            _snippet = find_element(r,By.XPATH,value='.//*[@class="gs_rs"]')
            snippet = _snippet.text if _snippet != None else ''
            self.res.append([title,link,snippet])
            # print(title,link)
            
        yield self.get(position=position+10)
            
            
        
        
        
    def __end__(self):
        self.end = True
        
    