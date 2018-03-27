#!/usr/bin/python
# -*- coding: utf-8 -*-

import exceptions
import time

# Dollar is taken as unit

cur_info = {'usd': {'cost': 1, 'symbol': '$', 'crypto': False}, 'eur': {'cost': 1.3,
	'symbol': ' EUR', 'crypto': False}, 'rub': {'cost': 0.016, 'symbol': '\u20bd', 'crypto': False},
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

		self.mining = None

		self.video_cards = []

	def buy_video_card(self, model, cur):
		self.update_money()

		if self.wallet[cur] < convert(video_card_info[model]['cost'], 'usd', cur):
			raise exceptions.TooExpensiveError(
				"video card '{0}' costs {1}{3}, but you have only {2}{3}".format(model,
					convert(video_card_info[model]['cost'], 'usd', cur), self.wallet[cur],
					cur_info[cur]['symbol']))

		self.wallet[cur] -= convert(video_card_info[model]['cost'], 'usd', cur)
		self.video_cards.append(model)

	def sell_video_card(self, model, cur):
		self.update_money()

		self.wallet[cur] += convert(video_card_info[model]['cost'], 'usd', cur)
		self.video_cards.remove(model)

	def exchange(self, money, cur1, cur2):
		self.update_money()

		ret = convert(money, cur1, cur2)

		self.wallet[cur1] -= money
		self.wallet[cur2] += ret

	def start_mining(self):
		if self.mining != None:
			raise exceptions.MiningError('mining has already begun at {}'.format(
				time.asctime(time.localtime(self.mining['start']))))

		mining = {} # Here will be info about mining
		mining['power'] = {}
		for cur in cur_info:
			if cur_info[cur]['crypto'] == False:
				continue

			mining['power'][cur] = 0

			for vc in self.video_cards:
				mining['power'][cur] += video_card_info[vc]['power'][cur]

		mining['start'] = int(time.time())

		self.mining = mining

	def stop_mining(self):
		self.update_money()
		self.mining = None

	def update_money(self):
		if self.mining == None:
			return

		for cur in self.mining['power']:
			self.wallet[cur] += self.mining['power'][cur] * (int(time.time()) - self.mining['start'])

		self.mining['start'] = int(time.time())

	def info(self):
		print('User:\t{} {} {}'.format(self.login, self.first_name, self.last_name))

		print()

		self.update_money()
		print('Wallet:')
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

	me.buy_video_card('vc1', 'usd')

	print('Before mining 3s:')
	me.info()

	me.start_mining()
	time.sleep(3)
	me.stop_mining()

	print('After mining 3s:')
	me.info()
