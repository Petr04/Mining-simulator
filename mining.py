import exceptions

cur_info = {'usd': {'cost': 1, 'symbol': '$', 'crypto': False}, 'eur': {'cost': 1.3,
	'symbol': ' EUR', 'crypto': False}, 'rub': {'cost': 0.016, 'symbol': ' RUB', 'crypto': False},
	'btc': {'cost': 10000, 'symbol': '\u20bf', 'crypto': True}, 'eth': {'cost': 2000,
	'symbol': ' ETH', 'crypto': True}}

video_card_info = {'vc1': {'power': {'btc': 0.000000001, 'eth': 0.000021}, 'cost': 200},
'vc2': {'power': {'btc': 0.000000017, 'eth': 0.000057}, 'cost': 317}}

def convert(summ, cur1, cur2):
	if cur1 in cur_info and cur2 in cur_info:
		return summ * (1 / cur_info[cur2]['cost']) * cur_info[cur1]['cost']
	else:
		raise exceptions.CurrencyError('no such currency')

class User:
	def __init__(self, login, passwd, first_name, last_name, btc, eth, usd, eur, rub):
		self.user_id = user_id
		self.first_name = first_name
		self.last_name = last_name

		self.money = {'usd': usd, 'eur': eur, 'rub': rub, 'btc': btc, 'eth': eth}

		self.mining = None

		self.video_cards = []

	def spend(self, summ, cur):
		if cur in cur_info:
			self.money[cur] -= summ
		else:
			raise exceptions.CurrencyError('no such currency')


	def get(self, summ, cur):
		if cur in cur_info:
			self.money[cur] += summ
		else:
			raise exceptions.CurrencyError('no such currency')

	def buy_video_card(self, model, cur):
		if model in video_card_info:
			if self.money[cur] < convert(video_card_info[model]['cost'], 'usd', cur):
				raise TooExpensiveError("video card '{0}' costs {1}{3}, but you have only {2}{3}".format \
					(model, video_card_info[model]['cost'][cur], self.money[cur], cur_info[cur][symbol]))

			self.spend(convert(video_card_info[model]['cost'], 'usd', cur), cur)
			self.video_cards.append(model)
		else:
			raise exceptions.VideoCardError("no video card named '{}'".format(model))

	def sell_video_card(self, model, cur):
		if model in video_card_info:
			self.get(convert(video_card_info[model]['cost'], 'usd', cur), cur)
			self.video_cards.remove(model)
		else:
			raise exceptions.VideoCardError('no video card named ' + model)

	def exchange(self, summ, cur1, cur2):
		ret = convert(summ, cur1, cur2)

		self.spend(summ, cur1)
		self.get(ret, cur2)

	def info(self):
		print('User:\t{} {} {}'.format(self.user_id, self.first_name, self.last_name))

		print()

		print('Money:')
		for i in self.money:
			print('\t{}{} crypto={}'.format(self.money[i], cur_info[i]['symbol'],
				cur_info[i]['crypto']))

		print()

		print('Video cards:\t{}'.format(self.video_cards))

if __name__ == '__main__':
	me = User(login = 'Petr04', passwd = 'qwerty', first_name = 'Petr', last_name = 'Makarov', btc = 0,
		eth = 0, usd = 300, eur = 0, rub = 0)

	print('Before buying video card:')
	me.info()

	me.buy_video_card('vc1', 'usd')

	print('After buying video card:')
	me.info()

	me.sell_video_card('vc1', 'usd')

	print('After selling video card:')
	me.info()
