import requests
from badger import Badger
from typing import Tuple, Optional, List

from util import *

class Scraper:
	@staticmethod
	def get_badgers() -> Tuple[Optional[List[Badger]], Optional[str]]:
		timer = Timer()
		print('getting badgers')

		url = 'https://ksfclzmasu.medianet.work/nft_for_sale?collection=boldbadgers'

		try:
			res = requests.get(url, timeout=7)
			if res.status_code != 200:
				return None, f'status not 200: {res.status_code}\n{res.content[:300]}'
		except Exception as e:
			return None, stack_trace(e)

		badgers = None
		try:
			badgers =  Badger.schema().loads(res.content, many=True)
		except Exception as e:
			return None, stack_trace(e)

		print(f'finished getting badgers {timer.time():.2f}s')

		return badgers, None
