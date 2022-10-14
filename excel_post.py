import argparse
from my_spider.tools import excel_post
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--excel', type=str)
parser.add_argument('--proxy',type=str,default=None,help='http://127.0.0.1:1087')
args = parser.parse_args()

excel_post(args.excel,proxy=args.proxy)