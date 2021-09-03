from util import stack_trace
from scraper import Scraper
from client import Client
from const import *

from badger import Badger

from typing import *
import threading
import copy
import time
import os
import pickle

from dotenv import load_dotenv
load_dotenv()

client = Client('starting...', channel_name='badger-bot')

def send_alarm(b: Badger, next: Optional[Badger]=None, channel='badger-bot'):
	client.send_message(
		'@everyone\n'+
		f'https://solanart.io/search/?token={b.token_add}\n'+
		'```'
		f'{b.name}\n'+
		f'rank : {ranks[b.name]}\n'
		f'price: {b.price:.3f} sol {f"(next is {next.price:.3f} sol)" if next is not None else ""}\n'+
		f'rare : {[a for a in b.attributes_list if percentages[a] <= 1.5]}\n'+
		f'attr : {[a for a in b.attributes_list]}\n'+
		f'count: {len(b.attributes_list) - 1}\n'+
		f'\n'+
		'```'
	, log=True, channel_name=channel)

sent = set()
try:
	with open('sent.pkl', 'rb') as f:
		sent = pickle.load(f)
except Exception as e:
	print(stack_trace(e))

def start():
	while not client.started:
		time.sleep(0.1)

	while True:
		badgers, err = Scraper.get_badgers()
		if err != None:
			print(err)
			continue
		rares = {a: [] for a, p in percentages.items() if p <= 1.5}
		for b in badgers:
			rare_count = 0
			for i, a in enumerate(b.attributes_list):
				if a == '':
					print(f'this one right here `{b.attributes}` {b.name}')
					continue
				if a not in percentages:
					print(f'missing attribute: `{a}` {b.name}')
					continue
				if percentages[a] <= 1.5:
					rares[a].append(copy.deepcopy(b))
					rare_count += 1
			if rare_count > 1:
				if (b.id, b.seller_address) not in sent:
					send_alarm(b)
					sent.add((b.id, b.seller_address))
					with open('sent.pkl', 'wb') as f:
						pickle.dump(sent, f)
			if len(b.attributes_list) in [1, 9]:
				if (b.id, b.seller_address) not in sent:
					send_alarm(b, channel='badger0178')
					sent.add((b.id, b.seller_address))
					with open('sent.pkl', 'wb') as f:
						pickle.dump(sent, f)
				
		for a, badgers in rares.items():
			if len(badgers) < 2:
				continue
			sorted_b = sorted(badgers, key=lambda x: x.price)
			b = sorted_b[0]
			if b.price <= 0.7 * sorted_b[1].price and (b.id, b.seller_address) not in sent:
				send_alarm(b, sorted_b[1], 'badger-bot-cheap-alarm')
				sent.add((b.id, b.seller_address))
				with open('sent.pkl', 'wb') as f:
					pickle.dump(sent, f)
		
t = threading.Thread(name='', target=start)
t.setDaemon(True)
t.start()

client.run(os.getenv('DISCORD_TOKEN'))