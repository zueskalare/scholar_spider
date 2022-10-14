import argparse

parse = argparse.ArgumentParser()
parse.add_argument('--web',type=str,default='https://scholar.google.com')
parse.add_argument('--keyword',type=str)
parse.add_argument('--number',type=int,default=100)
parse.add_argument('--mark',type=str,default='')
parse.add_argument('--year',type=str,default=None)
parse.add_argument('--sort',type=str,default='relevance',help='date or relevance or date_everything')
parse.add_argument('--proxy',type=str,default=None,help='http://127.0.0.1:1087')

opt = parse.parse_args()

from my_spider.my_spider import crawl
from my_spider.tools import excel_post
import pandas as pd


cr =crawl(web=opt.web,key_word=opt.keyword,proxy=opt.proxy,year=opt.year,sort=opt.sort,number=opt.number)

res = cr.get()
num = cr.number
print('all number',num)

for i in range(0,num,10):
    try:
        print(i)
        res = res.__next__()
    except KeyboardInterrupt:
        print('ending')
        break

# print(cr.res)
out =  opt.keyword.replace(' ','_')+'+'+opt.mark
engine = pd.ExcelWriter(out+'.xlsx')
frame = pd.DataFrame(cr.res,columns=cr.index)
frame.to_excel(excel_writer=engine)
engine.close()

excel_post(out+'.xlsx',proxy=opt.proxy)

