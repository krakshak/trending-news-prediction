import requests
import re
import pandas as pd

import ipdb;ipdb.set_trace()
trending_news_url = "https://timesofindia.indiatimes.com/viral-news"
response = requests.get(trending_news_url)

block_regex = '''<div class="content-wrapper 2">(.*?)</span></div></li>'''
title_regex = '''title="(.*?)"'''
desc_regex = '''"w_desc">(.*?)</span>'''

news_list = list()

try:
	if response.status_code == 200:
		page_blocks = re.findall(block_regex,response.content.decode('utf-8'))
		for pb in page_blocks:
			news_obj = dict()
			news_obj["title"] = re.search(title_regex,pb).group(1)
			news_obj["desc"] = re.search(desc_regex,pb).group(1)
			news_list.append(news_obj)

		df = pd.DataFrame(news_list)

except:
	pass

	
	