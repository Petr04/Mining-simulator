class CurrencyError(Exception):
	pass

class TooExpensiveError(CurrencyError):
	pass

class MiningError(Exception):
	pass
