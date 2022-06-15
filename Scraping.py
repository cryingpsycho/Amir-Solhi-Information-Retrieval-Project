#Importing the libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

#Body of code
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
scraped_data = []

for i in tqdm(range (1,40)):
	url=f'https://news.ycombinator.com/news?p={i}'
	response=requests.get(url,headers=headers)
	soup=BeautifulSoup(response.content,'html5lib')
	for item in soup.find_all('tr'):
		try:
			if item.select('.rank'):
				rank=item.select('.rank')[0].get_text()
			if item.select('.titlelink'):
				page_url=item.select('.titlelink')[0]['href']
				if page_url.find('item?id=') == 0 : page_url=f'https://news.ycombinator.com/{page_url}'
				title=item.select('.titlelink')[0].get_text()
				scraped_data.append({'rank': rank, 'url': page_url, 'title':title})
				
			if item.select('.score'):
				username = item.select('.hnuser')[0].get_text()
				score = item.select('.score')[0].get_text()
				comments =item.find_all('a')[3].get_text()
				age =item.find_all('a')[1].get_text()
				if comments == 'discuss' or comments == 'hide':comments='0 comments'
				scraped_data.append({'rank': rank, 'url': page_url, 'title':title, 'user':username, 'score':score, 'comments':comments,'age':age})
		
		except Exception as e:
			raise e
			print('')

#Export
df = pd.DataFrame(scraped_data)
dfd= df.drop_duplicates(subset=['rank'], keep='last', ignore_index=True)
dfd.to_csv(f'hackernews.csv')
#df.to_csv(f'hackernews2.csv')