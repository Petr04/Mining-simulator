class CurrencyError(Exception):
	pass

class TooExpensiveError(CurrencyError):
	pass

class VideoCardError(Exception):
	pass

class MiningError(Exception):
	pass
