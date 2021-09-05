import requests
import re
import pandas as pd
import json

def news_crawler(listing_url):
	urls = list()
	news_list = list()
	
	#regexes
	html_url_regex = '''<a\s*href="(.*?)"\s*class="component_2">'''
	title_regex = '''id="article_title">(.*?)</title>'''
	desc_regex = '''name=description\s*content="([^>]*?)\s*">'''
	#import ipdb;ipdb.set_trace()

	try:
		#Crawling till 25 pages
		for i in range(0,25):
			listing_request_url = listing_url+str("/")+str(i)
			print(listing_request_url)
			
			#request to the listing page
			response = requests.get(listing_request_url)
			
			if response.status_code == 200:
				if str("<html") in response.content.decode():
					urls = re.findall(html_url_regex,response.content.decode('utf-8'))
					if "trending-news" in listing_url:
						urls = [str("https://www.timesnownews.com")+str(u) for u in urls]
					for url in urls:
						if "video" in url:
							continue
						presp = requests.get(url)
						news_obj = dict()
						news_obj["title"] = re.search(title_regex,presp.content.decode('utf-8')).group(1)
						news_obj["desc"] = re.search(desc_regex,presp.content.decode('utf-8')).group(1)
						news_list.append(news_obj)
					#print("fetched page data using HTML page")

				else:
					if "trending-news" in listing_url:
						json_data = json.loads(response.content.decode('utf-8')).get("popular_stories")
						urls = [str("https://www.timesnownews.com")+str(u.get("story_url")) for u in json_data]
					if "latest-news" in listing_url:
						json_data = json.loads(response.content.decode('utf-8')).get("latest_stories")
						urls = [str(u.get("story_url")) for u in json_data]
					for url in urls:
						presp = requests.get(url)
						news_obj = dict()
						news_obj["title"] = re.search(title_regex,presp.content.decode('utf-8')).group(1)
						news_obj["desc"] = re.search(desc_regex,presp.content.decode('utf-8')).group(1)
						news_list.append(news_obj)
					print("fetched page data using API page")
		
		#constructing news dataframe
		df = pd.DataFrame(news_list,columns=["title","desc"])

	except:
		pass

	return df

trending_news = "https://www.timesnownews.com/trending-news"
non_trending_news = "https://www.timesnownews.com/latest-news"

trending_df = news_crawler(trending_news)
trending_df.to_csv('trending_news.csv', encoding='utf-8', index=False)

non_trending_df = news_crawler(non_trending_news)
non_trending_df.to_csv('non_trending_news.csv', encoding='utf-8', index=False)