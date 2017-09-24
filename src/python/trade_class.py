import time
import datetime
import configparser
import api
class account:
	poloniex = api.poloniex("A", "B")
	apikey = ""
	secret = ""
	currency = {}
	aggression = 0.0



	balances = {}
	openOrders = []

	def __init__(self):
		config = configparser.ConfigParser()
		config.read("config.txt")
		self.secret = config["user"]["Secret"]
		self.apikey = config["user"]["API"]
		self.aggression = float(config["user"]["aggression"])
		self.currency["currencyPair"] = config["user"]["currency"] #The API likes this format

		self.connect()
		self.updateBalances()

	def getBalances(self):
		self.updateBalances()
		return self.balances

	def getAggression(self):
		return self.aggression

	def getCurrency(self):
		return self.currency

	def updateBalances(self):
		try:
			self.balances = self.poloniex.returnBalances()
		except:
			print("Unsuccesful at updating balances,", self.balances)
		relevantBalances = dict(self.balances)
		relevant = self.currency["currencyPair"].split("_")
		for key, val in relevantBalances.items():
			if key not in relevant:
				del self.balances[key]

	def getAPI(self):
		return self.poloniex

	def connect(self):
		self.poloniex = api.poloniex(self.apikey, self.secret)

	def buy(self, amount, rate, reason):
		print("BUYYINNG")
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		try:
			id = self.poloniex.buy(self.currency['currencyPair'], rate, amount)
			print("Problem buying: ", id)
		except:
			return
		if "orderNumber" not in id:
			print("Unsuccesful buy")
			print(id)
			print(self.balances, amount)
			return
		id = id["orderNumber"]
		self.openOrders += [trades(id, amount, rate, "buy", reason, timestamp, 0)]
	
	def sell(self, amount, rate, reason):
		print("SELLING")
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		try:
			id = self.poloniex.sell(self.currency['currencyPair'], rate, amount)
			print("Problem selling: ", id)
		except:
			return
		if "orderNumber" not in id:
			print("Unsuccesful sell")
			print(id)
			print(self.balances, amount)
			return
		id = id["orderNumber"]
		self.openOrders += [trades(id, amount, rate, "sell", reason, timestamp, 0)]
		
	def updateOrders(self):
		polorders = self.poloniex.returnOpenOrders(self.currency['currencyPair'])
		copyOrders = list(self.openOrders)
		for polo in polorders:
			for my in self.openOrders:
				if polo["orderNumber"] == my.orderNumber:
					copyOrders.remove(my)

		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		for i in copyOrders:
			i.selldate = timestamp
		out = []
		for i in copyOrders:
			out += [i.insert_sql()]
		return out


class trades:
	orderNumber = 0
	amount = 0
	rate = 0
	type = ""
	reason = ""
	creationdate = 0
	selldate = False


	def __init__(self, nid, namount, nrate, ntype, nreason,  ndate, nselldate):
		self.orderNumber = nid
		self.amount = namount
		self.rate = nrate
		self.type = ntype
		self.reason = nreason
		self.creationdate = ndate
		self.selldate = nselldate

	def insert_sql(self):
		return str("INSERT INTO mytrades (amount, rate, type, creationdate, selldate, reason) VALUES (" + str(self.amount) + ", " + str(self.rate) + ", '" + self.type +  "', '" + self.creationdate  + "', '" + self.selldate + "', '" + self.reason + "');") 


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


class MACD:
	MACDVal = 0
	EMA9 = 0
	time = 0
	curtype = ""

	def __init__(self, MACDVal, EMA9, time, curtype):
		self.MACDVal = MACDVal
		self.EMA9 = EMA9
		self.time = time
		self.curtype = curtype

	def insert_sql(self):
		return str("INSERT INTO macd (macd, ema9, time, type) VALUES (" + str(self.MACDVal) + "," + str(self.EMA9) + ", '" + str(self.time) + "' , '" + str(self.curtype) + "');")
