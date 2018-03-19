import exceptions

cur_info = {'usd': {'cost': 1, 'symbol': '$', 'crypto': False}, 'eur': {'cost': 1.3,
	'symbol': ' EUR', 'crypto': False}, 'rub': {'cost': 0.016, 'symbol': ' RUB', 'crypto': False},
	'btc': {'cost': 10000, 'symbol': '\u20bf', 'crypto': True}, 'eth': {'cost': 2000,
	'symbol': ' ETH', 'crypto': True}}

video_card_info = {'vc1': {'power': {'btc': 0.000000001, 'eth': 0.000021}, 'cost': 200},
'vc2': {'power': {'btc': 0.000000017, 'eth': 0.000057}, 'cost': 317}}

def convert(money, cur1, cur2):
	if not(cur1 in cur_info and cur2 in cur_info):
		raise exceptions.CurrencyError('no such currency')

	return money * (1 / cur_info[cur2]['cost']) * cur_info[cur1]['cost']

class User:
	def __init__(self, login, passwd, first_name, last_name, wallet):
		self.login = login
		self.passwd = passwd

		self.first_name = first_name
		self.last_name = last_name

		self.wallet = wallet

		self.video_cards = []

	def buy_video_card(self, model, cur):
		if not(model in video_card_info):
			raise exceptions.VideoCardError("no video card named '{}'".format(model))

		if self.wallet[cur] < convert(video_card_info[model]['cost'], 'usd', cur):
			raise exceptions.TooExpensiveError(
				"video card '{0}' costs {1}{3}, but you have only {2}{3}".format(model,
					convert(video_card_info[model]['cost'], 'usd', cur), self.wallet[cur],
					cur_info[cur]['symbol']))

		self.wallet[cur] -= convert(video_card_info[model]['cost'], 'usd', cur)
		self.video_cards.append(model)

	def sell_video_card(self, model, cur):
		if not(model in self.video_cards):
			raise exceptions.VideoCardError(
				"user {} hasn't video card named '{}'".format(self.name, model))

		self.wallet[cur] += convert(video_card_info[model]['cost'], 'usd', cur)
		self.video_cards.remove(model)

	def exchange(self, money, cur1, cur2):
		ret = convert(money, cur1, cur2)

		self.wallet[cur1] -= money
		self.wallet[cur2] += ret

	def info(self):
		print('User:\t{} {} {}'.format(self.login, self.first_name, self.last_name))

		print()

		print('wallet:')
		for i in self.wallet:
			print('\t{}{} crypto={}'.format(self.wallet[i], cur_info[i]['symbol'],
				cur_info[i]['crypto']))

		print()

		print('Video cards:\t{}'.format(self.video_cards))

if __name__ == '__main__':
	wallet = {}
	wallet = dict.fromkeys(list(cur_info.keys()), 0)
	# Making dict with currency names from cur_info. Here will be info about user's money.

	wallet['usd'] = 300

	me = User(login = 'Petr04', passwd = 'qwerty', first_name = 'Petr', last_name = 'Makarov',
		wallet = wallet)

	print('Before buying video card:')
	me.info()

	me.buy_video_card('vc1', 'usd')

	print('After buying video card:')
	me.info()

	me.sell_video_card('vc1', 'usd')

	print('After selling video card:')
	me.info()
