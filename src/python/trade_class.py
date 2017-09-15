import time
import datetime

class trades:
	id = 0
	amount = 0
	rate = 0
	type = ""
	creationdate = 0
	selldate = False

	def __init__(self, nid, namount, nrate, ntype, ndate, nselldate):
		self.id = nid
		self.amount = namount
		self.rate = nrate
		self.type = ntype
		self.creationdate = ndate
		self.selldate = nselldate


class condensed_trades:
	rate = 0
	type = ""
	date = 0

	def __init__(self, nrate, ntype, ndate):
		self.rate = nrate
		self.type = ntype
		self.date = ndate

class ticker:
	quoteVol = 0
	high24 = 0
	baseVol = 0
	low24 = 0
	HighBid = 0
	last = 0
	lowestAsk = 0
	percentChange = 0
	time = 0
	curtype = ""

	def __init__(self, nquote, nhigh, nbase, nlow, nhighbid, nlast, nlowestAsk, npercentChange):
		self.quoteVol = nquote
		self.high24 = nhigh
		self.baseVol = nbase
		self.low24 = nlow
		self.HighBid = nhighbid
		self.last = nlast
		self.lowestAsk = nlowestAsk
		self.percentChange = npercentChange

	def __init__(self, map, ntime, ncurtype):
		self.quoteVol = map["quoteVolume"]
		self.high24 = map["high24hr"]
		self.baseVol = map["baseVolume"]
		self.low24 = map["low24hr"]
		self.HighBid = map["highestBid"]
		self.last = map["last"]
		self.lowestAsk = map["lowestAsk"]
		self.percentChange = map["percentChange"]
		self.time = ntime
		self.curtype = ncurtype

	def insert_sql(self):
		return str("INSERT INTO ticker (quoteVol, high24, baseVol, low24, HighBid, last, lowestAsk, percentChange, type, date) VALUES (" \
			+ str(self.quoteVol) +", " + str(self.high24) +", " + str(self.baseVol) +", " + str(self.low24) +", " + \
			 str(self.HighBid) +", " + str(self.last) +", " + str(self.lowestAsk) +", " + str(self.percentChange) + ", " \
			  + str(0) + ", '" + self.time + "');")

