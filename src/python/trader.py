#from Crypto.Cipher import AES
import api
#import base64
import json
#import io
#import encrypt
import pymysql.cursors
from collections import deque
import time
import datetime
import trade_class
import math
import multiprocessing

# Connect to the database
connection = pymysql.connect(host='localhost',
							 user='trader',
							 password='Immabigfatjuicypassword',
							 db='crypto')

OrdersLock = multiprocessing.Lock()
SMA1Lock = multiprocessing.Lock()
SMA50Lock = multiprocessing.Lock()
SMA200Lock = multiprocessing.Lock()
StdDevLock = multiprocessing.Lock() # why are these here and in main?
currency = {}
currency["currencyPair"] = "USDT_ETH" #The API likes this format


# """
# Calculates a 50 and 200 day Simple moving average.
# Loops forever
# Both parameters must be type manager.Value('d', 0.0)
# """
def SMA(waitEvent, SMA1, SMA50, SMA200, StdDev, EMA9, MACD):
	waitEvent.clear()
	p = api.poloniex("A", "B") #Gonna have to populate this with a APIkey in pass eventually
	top_tick_events = []
	#bottom_tick_events = []
	try:
		with connection.cursor() as cursor:

			#Uncomment this section to load trades from poloneix dump
			#This sits in the "history.json" file
			#load up old trades

			# """start = time.time()
			# data  = {}
			# with open('history.json', 'r') as fp:
			# 	data = json.load(fp)
			# print ("Done reading")
			# for k in data:	#																															quoteVol, 							high24, 			baseVol,					 low24, 						HighBid, 					last, 					lowestAsk,			percentChange, 		type, date)								
			# 	ts = int(k["date"])
			# 	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			# 	cursor.execute("INSERT INTO ticker (quoteVol, high24, baseVol, low24, HighBid, last, lowestAsk, percentChange, type, date) VALUES  (" + str(k["quoteVolume"]) + ", " + str(k["high"]) + ','  + str(k["volume"]) + ',' + str(k["quoteVolume"]) + ','  + str(k["low"]) + ','  + str(k["weightedAverage"])  + ','+ str(k["low"])  + ',' + "0" + ','  +"'all'"+  ",'"+timestamp +"')")

			# print("done in " + str(time.time() - start))
			# connection.commit()
			# quit()
			# """
			print("Pulling old data from DB and calculating averages")
			cursor.execute("Select last from ticker  WHERE date >= ( CURDATE() - INTERVAL 2 DAY ) ORDER BY date ASC;") #Pull the last day from DB
			bottom_tick_events = deque(cursor.fetchall())
			for i in bottom_tick_events:
				SMA1.value += i[0]
			SMA1.value /= len(bottom_tick_events) #Average that shit
			cursor.execute("Select last from ticker  WHERE date >= ( CURDATE() - INTERVAL 200 DAY ) ORDER BY date ASC;") #Pull the last 200 days from DB
			bottom_tick_events200 = deque(cursor.fetchall())
			stdDevNum = 0.0
			for i in bottom_tick_events200:
				SMA200.value += i[0]
			SMA200.value /= len(bottom_tick_events200) #Average that shit
			cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 50 DAY ) ORDER BY date ASC;") #Pull the last 50 days from DB
			bottom_tick_events50 = deque(cursor.fetchall())
			for i in bottom_tick_events50:
				SMA50.value += i[0] #repeate
			SMA50.value /= len(bottom_tick_events50)
			for i in bottom_tick_events50:
				stdDevNum += (i[0]-SMA50.value)**2 # rerun the loop to get standard deviations
			StdDev.value = (stdDevNum/(len(bottom_tick_events50)))**(1/2)
			lenSMA50= len(bottom_tick_events50) #see how many events that took for each
			lenSMA200= len(bottom_tick_events200)
			lenSMA1  = len(bottom_tick_events)

			cursor.execute("Select last,date from ticker WHERE date >= ( CURDATE() - INTERVAL 26 DAY ) ORDER BY date ASC;") #Pull the last 26 days from DB
			bottom_tick_eventsEMA26 = deque(cursor.fetchall())
			
			cursor.execute("Select last,date from ticker WHERE date >= ( CURDATE() - INTERVAL 12 DAY ) ORDER BY date ASC;") #Pull the last 12 days from DB
			bottom_tick_eventsEMA12 = deque(cursor.fetchall())
			
			cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 9 DAY ) ORDER BY date ASC;") #Pull the last 9 days from DB
			bottom_tick_eventsEMA9 = deque(cursor.fetchall())
			
			EMA26 = bottom_tick_eventsEMA26.popleft()[0]
			EMA12 = bottom_tick_eventsEMA12.popleft()[0]
			#EMA9.value = bottom_tick_eventsEMA9.popleft()[0]

			macdlist = []

			alpha26 = 2.0 / (26 + 1)
			alpha12 = 2.0 / (12 + 1)
			alpha9 = 2.0 / (9 + 1)
			print(alpha26, alpha12, alpha9)
			while len(bottom_tick_eventsEMA26) > 0:
				val = bottom_tick_eventsEMA26.popleft()
				EMA26 = (alpha26 * val[0]) + (1 - alpha26) * EMA26
				EMA12 = (alpha12 * val[0]) + (1 - alpha12) * EMA12
				macdlist += [trade_class.MACD(EMA12 - EMA26,0, val[1], currency["currencyPair"])]

			EMA9.value = macdlist[0].MACDVal
			for i in macdlist:
				EMA9.value = (alpha9 * i.MACDVal) + (1 - alpha9) * EMA9.value
				i.EMA9 = EMA9.value

			MACD.value = macdlist[-1].MACDVal # most recent macd, makes sense
			for i in macdlist:
				cursor.execute("Select macd from macd WHERE time = '" + str(i.time) +"'" ) # grab the macd value in our db for this time
				if len(cursor.fetchall()) == 0: # if there isn't a value in our database, commit one. This makes us skip duplicates?
					cursor.execute(i.insert_sql())
			connection.commit()

			macdlist = []
			waitEvent.set()
			while True : #And repeat forever
				print("calculation loop")
				time.sleep(3) #The number changes pretty slowly, and even 3 seconds produces a lot of duplicates
				liveDev = ((StdDev.value)**2)*lenSMA50 #this number is useful for live standard deviation calculations
				ts = time.time()
				timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') #Convert to date-time
				try:
					query  = p.api_query("returnTicker") #Run the ticker event

				except:
					print("A stupid exception occured")
					continue

				query = query[currency["currencyPair"]] #We only care about the current trading value, "USDT_ETH"
				top_tick_events += [trade_class.ticker(query, timestamp, currency["currencyPair"])] #Add it to a list of the past ticker events
				oldAve = SMA50.value
				SMA50.value += (float(query["last"]) - bottom_tick_events50.popleft()[0]) / lenSMA50 #SMA that shit
				SMA200.value += (float(query["last"]) - bottom_tick_events200.popleft()[0]) / lenSMA200
				SMA1.value += (float(query["last"]) - bottom_tick_events.popleft()[0]) / lenSMA1

				EMA12 = (alpha12 * float(query["last"])) + (1 - alpha12) * EMA12
				EMA26 = (alpha26 * float(query["last"])) + (1 - alpha26) * EMA26
				
				MACD.value = EMA12 - EMA26
				EMA9.value = (alpha9 * MACD.value) + (1 - alpha9) * EMA9.value
				macdlist += [trade_class.MACD(MACD.value, EMA9.value, timestamp, currency["currencyPair"])]
				liveDev -= (bottom_tick_events50.popleft()[0]-SMA50.value)*(bottom_tick_events50.popleft()[0] - oldAve)
				liveDev += (float(query["last"])-SMA50.value)*(float(query["last"]) - oldAve)
				StdDev.value = (liveDev/lenSMA50)**(1/2)
				if len(top_tick_events) == 100: #When that list of events gets to 100, flush it and send it to MYSQL

					cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 200 DAY ) ORDER BY date ASC LIMIT 100") #Check my logic on this
					bottom_tick_events200 = deque(cursor.fetchall()) #Get the last 100 events. We cycle in 100 for the SMA math, and cycle out 1 event each iteration
																	# I think it'll work when we have a more consistent data set
					cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 50 DAY ) ORDER BY date ASC LIMIT 100")
					bottom_tick_events50 = deque(cursor.fetchall())

					cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 2 DAY ) ORDER BY date ASC LIMIT 100")
					bottom_tick_events = deque(cursor.fetchall())

					print("Flushing to database") #write it all to sql
					for i in top_tick_events:
						cursor.execute(i.insert_sql());
					for i in macdlist:
						cursor.execute(i.insert_sql())
				
					connection.commit()
					macdlist = []
					top_tick_events = []
		
	finally:
		connection.close()

#This function takes our indicators and puts thought into them
#I want to structure this as a series of watchdog functions
def TradeBrain(SMA1, SMA50, SMA200, StdDev, EMA9, MACD):
	print("Thinking about what to trade.")
	wcondition1 = False
	wcondition2 = False
	wcondition3 = False
	mcondition1 = False
	mcondition2 = False
	mcondition3 = False
	firstHumpW = 0.0
	indicator = 0.0
	wasPositive = False
	wasNegative = False
	while True:
	#section 1 is a W pattern
		if SMA1.value < SMA50.value - (2*StdDev.value):
			wcondition1 = True
		if SMA1.value > SMA50.value:
			firstHumpW = SMA1.value
			wcondition2 = wcondition1
		#check for false signals
		if wcondition1 and wcondition2 and wcondition3 and SMA1.value > SMA50.value + (2*StdDev.value):
			wcondition1 = False
			wcondition2 = False
			wcondition3 = False
			firstHumpW = 0.0
		if SMA1.value < SMA50.value and SMA1.value > SMA50.value - (2*StdDev.value) and SMA1.value < firstHumpW:
			wcondition3 = wcondition2
			wcondition1 = wcondition2
		if wcondition3 and SMA1.value > SMA50.value + (2*StdDev.value):
			wcondition1 = False
			wcondition2 = False
			wcondition3 = False
			firstHumpW = 0.0
			print("W pattern recommends buying now at roughly ", SMA1.value)
	#section 2 is an M pattern
		if SMA1.value > SMA50.value + (2*StdDev.value):
			mcondition1 = True
		if SMA1.value < SMA50.value:
			mcondition2 = mcondition1
		#check for false signals
		if mcondition1 and mcondition2 and mcondition3 and SMA1.value < SMA50.value - (2*StdDev.value):
			mcondition1 = False
			mcondition2 = False
			mcondition3 = False
		if SMA1.value > SMA50.value and SMA1.value < SMA50.value + (2*StdDev.value):
			mcondition3 = mcondition2
			mcondition1 = mcondition2
		if mcondition3 and SMA1.value < SMA50.value - (2*StdDev.value):
			mcondition1 = False
			mcondition2 = False
			mcondition3 = False
			print("M pattern recommends selling now at roughly ", SMA1.value)
	#section 3 is an EMA move
	#if EMA is
		wasPositive = indicator > 0
		wasNegative = indicator < 0
		indicator = MACD.value - EMA9.value
		if math.isclose(float(indicator), float(0.0), abs_tol = .1):
			if wasNegative:
				print("EMA pattern recommends buying now at roughly ", SMA1.value)
			elif wasPositive:
				print("EMA pattern recommends selling now at roughly ", SMA1.value)

#This tracks bids and asks to SQL. I kinda hate it. But we gotta have it!
def TrackandInsertOpenOrders():
	p = api.poloniex("A", "B")
	currency = {}
	currency["currencyPair"] = "USDT_ETH"
	OpenOrders = {}
	OpenOrders['bids'] = {}
	OpenOrders['asks'] = {}
	try:
		with connection.cursor() as cursor:
			curtime = time.time() + 60


			#load up old trades
			sql = "select * from trades"
			cursor.execute(sql)
			result = cursor.fetchall()
			for i in result:
				print(i)
				OrderBook[i[3]][i[0]] = trade_class.trades(i[0],i[1],i[2],i[3],i[4],False)
			sql = "INSERT INTO trades (amount, rate, type, date) VALUES "#(%f, %f, %s, %s)
				
			while True :
				print("begin")
				curtime = time.time() + 60
				time.sleep(0.5)

				query  = p.api_query("returnOpenOrders", currency)
				
				ts = time.time()
				timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				OpenOrdersTemp = OpenOrders.copy()
				NewTrades = []
				for i in query['bids']:
						for key, value in OpenOrdersTemp['bids'].items():
							if math.isclose(float(value.amount), float(i[1]), abs_tol=0.05) and math.isclose(float(value.rate), float(i[0]), abs_tol=0.05):
								del OpenOrdersTemp['bids'][key]
								query['bids'].remove(i)
								break

				for i in query['asks']:
						for key, value in OpenOrdersTemp['asks'].items():
							#pass
							if math.isclose(float(value.amount), float(i[1]), abs_tol=0.05) and math.isclose(float(value.rate), float(i[0]), abs_tol=0.05):
								print("removing", key)
								del OpenOrdersTemp['asks'][key]
								query['asks'].remove(i)
								break
				print("end checking")
				#remove old values from SQL and active list
				for key,value in OpenOrdersTemp['bids'].copy().items():
					del OpenOrders['bids'][key]
					cursor.execute("update trades set selldate = '" + timestamp + "' where id = " + str(key))
				for key,value in OpenOrdersTemp['asks'].copy().items():
					del OpenOrders['asks'][key]
					cursor.execute("update trades set selldate = '" + timestamp + "' where id = " + str(key))
				print("end pruning")
				#insert new values into SQL
				for i in query['bids']:
					data = sql + "("+ str(i[1]) + ", " + str(i[0]) + ", 'bids', '" + timestamp +"');"
					cursor.execute(data)
					connection.commit()
					cursor.execute("SELECT MAX(id) FROM trades;")
					newid = cursor.fetchone()[0]
					OpenOrders["bids"][newid] = trade_class.trades(newid, i[1], i[0], "bids", timestamp, 0)
				for i in query['asks']:
					data = sql + "("+ str(i[1]) + ", " + str(i[0]) + ", 'asks', '" + timestamp +"');"
					cursor.execute(data)
					connection.commit()
					cursor.execute("SELECT MAX(id) FROM trades;")
					newid = int(cursor.fetchone()[0])
					OpenOrders["asks"][newid] = trade_class.trades(newid, i[1], i[0], "bids", timestamp, 0)
				print("commit")
				connection.commit()
				# """	data = sql + "("+ str(i[1]) + ", " + str(i[0]) + ", 'USDT_ETH', '" + timestamp +"');"
				# 	print(data)
				# 	cursor.execute(data)
				# connection.commit()
				# quit()
				# """
	finally:
		connection.close()


# """
# Get the current Orderbook of bids and asks
# OpenOrders must be a manager.dict()
# e is a multiprocessing.Event()
# Cycling every half second for no good reason
# """
def getOpenBook(OpenOrders, e):
	e.clear()
	print("Openbook Started")
	p = api.poloniex("A", "B")
	while True :
		print("open book loop")
		e.clear() #clear the event. Make em wait
		OpenOrders['bids'] = p.api_query("returnOrderBook", currency)['bids']
		OpenOrders['asks'] = p.api_query("returnOrderBook", currency)['asks']
		e.set() #Set the event. This ends anything calling ".wait()" and lets that function continue on
		time.sleep(0.5)

#init some shit
def init(O, S1, S5, S2, SD):
	global OrdersLock, SMA1Lock, SMA50Lock, SMA200Lock
	OrdersLock = O
	SMA1Lock = S1
	SMA50Lock = S5
	SMA200Lock = S2
	StdDevLock = SD

def main():
	manager = multiprocessing.Manager() #This sets up a server that controls processing events
	e = multiprocessing.Event()
	waitEvent = multiprocessing.Event()

	OrdersLock = multiprocessing.Lock()
	SMA1Lock = multiprocessing.Lock()
	SMA50Lock = multiprocessing.Lock()
	SMA200Lock = multiprocessing.Lock()
	StdDevLock = multiprocessing.Lock()
	pool = multiprocessing.Pool(initializer=init, initargs=(OrdersLock, SMA1Lock, SMA50Lock, SMA200Lock, StdDevLock)) #Run the init function
	print("Setting up")
	SMA1 = manager.Value('d', 0.0)
	SMA50 = manager.Value('d', 0.0)
	SMA200 = manager.Value('d', 0.0)
	MACD = manager.Value('d', 0.0)
	EMA9 = manager.Value('d', 0.0)
	StdDev = manager.Value('d', 0.0)
	OpenOrders = manager.dict()
	print("Spawning processes")
	OpenbookProcess = multiprocessing.Process(target=getOpenBook, args=(OpenOrders, e)) #Spawn some new processes
	OpenbookProcess.start()
	SMAProcess = multiprocessing.Process(target=SMA, args=(waitEvent, SMA1, SMA50, SMA200, StdDev, EMA9, MACD))
	SMAProcess.start()
	TradeProcess = multiprocessing.Process(target=TradeBrain, args=(SMA1, SMA50, SMA200, StdDev, EMA9, MACD))
	TradeProcess.start()
	waitEvent.wait() #Wait until a SMA is finished setting up

	print("Looping")
	while True:
		print("Main loop\n")
		time.sleep(0.75)
		

		for i in OpenOrders['bids']:
			if SMA50.value < float(i[0]):
				pass
				#print(i[0], ": bid detected greater than 50 day average: ", SMA50.value)
		print("SMA1", SMA1.value)
		print("SMA50", SMA50.value)
		print("SMA200", SMA200.value)
		print("MACD", MACD.value)
		print("EMA9", EMA9.value)
		print("StdDev", StdDev.value)
main()
