from apikey import key
import requests

def convert(amount, cur_1, cur_2, rates):
	return amount * rates['rates'][cur_2] / rates['rates'][cur_1]

def change_base(new_base, rates):
	for cur in rates['rates']:
		rates['rates'][cur] = convert(1, cur, new_base, rates)

	base = new_base
