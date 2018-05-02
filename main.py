#!/usr/bin/python
# -*- coding: utf-8 -*-

import exceptions
import time
from convert import *
import requests
from apikey import key

# EUR is taken as unit

rates = requests.get('http://data.fixer.io/api/latest?access_key={}'.format(key)).json()
crypto = ['BTC']

video_card_info = {'vc1': {'power': {'BTC': 0.000000001}, 'cost': 200},
'vc2': {'power': {'BTC': 0.000000017}, 'cost': 317}}

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

		if self.wallet[cur] < convert(video_card_info[model]['cost'], 'EUR', cur, rates):
			raise exceptions.TooExpensiveError(
				"video card '{0}' costs {1}{3}, but you have only {2}{3}".format(model,
					convert(video_card_info[model]['cost'], 'EUR', cur, rates), self.wallet[cur],
					cur))

		self.wallet[cur] -= convert(video_card_info[model]['cost'], 'EUR', cur, rates)
		self.video_cards.append(model)

	def sell_video_card(self, model, cur):
		self.update_money()

		self.wallet[cur] += convert(video_card_info[model]['cost'], 'EUR', cur, rates)
		self.video_cards.remove(model)

	def exchange(self, money, cur_1, cur_2):
		self.update_money()

		ret = convert(money, cur_1, cur_2, rates)

		self.wallet[cur_1] -= money
		self.wallet[cur_2] += ret

	def start_mining(self):
		if self.mining != None:
			raise exceptions.MiningError('mining has already begun at {}'.format(
				time.asctime(time.localtime(self.mining['start']))))

		mining = {} # Here will be info about mining
		mining['power'] = {}
		for cur in rates['rates']:
			if not (cur in crypto):
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
		for cur in self.wallet:
			print('\t{} {} crypto: {}'.format(self.wallet[cur], cur, cur in crypto))

		print()

		print('Video cards:\t{}'.format(self.video_cards))

if __name__ == '__main__':
	wallet = {}
	wallet = dict.fromkeys(list(rates['rates'].keys()), 0)
	# Making dict with currency names. Here will be info about user's money.

	wallet['EUR'] = 300

	me = User(login = 'Petr04', passwd = 'qwerty', first_name = 'Petr', last_name = 'Makarov',
		wallet = wallet)

	me.buy_video_card('vc1', 'EUR')

	print('Before mining 3s:')
	me.info()

	me.start_mining()
	time.sleep(3)
	me.stop_mining()

	print('After mining 3s:')
	me.info()
