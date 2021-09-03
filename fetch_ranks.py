import requests
import bs4
import pickle

ranks = {}

for i in range(40):
	resp = requests.get('https://howrare.is/boldbadgers/?sort_by=rank&page='+str(i))
	soup = bs4.BeautifulSoup(resp.content)
	data = soup.find_all('div', class_='nft-details')
	for d in data:
		name = d.find('h3').text
		rank = d.find('strong').text
		print(name, rank)
		ranks[name] = rank
	
with open('ranks.pkl', 'wb') as f:
	pickle.dump(ranks, f)