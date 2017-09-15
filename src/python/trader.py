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
SMA50Lock = multiprocessing.Lock()
SMA200Lock = multiprocessing.Lock()
currency = {}
currency["currencyPair"] = "USDT_ETH" #The API likes this format


"""
Calculates a 50 and 200 day Simple moving average.
Loops forever
Both parameters must be type manager.Value('d', 0.0)
"""
def SMA(SMA50, SMA200):
	p = api.poloniex("A", "B")
	top_tick_events = []
	bottom_tick_events = []
	try:
		with connection.cursor() as cursor:

			#Uncomment this section to load trades from poloneix dump
			#This sits in the "history.json" file
			#load up old trades

			"""start = time.time()
			data  = {}
			with open('history.json', 'r') as fp:
				data = json.load(fp)
			print ("Done reading")
			for k in data:	#																															quoteVol, 							high24, 			baseVol,					 low24, 						HighBid, 					last, 					lowestAsk,			percentChange, 		type, date)								
				ts = int(k["date"])
				timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				cursor.execute("INSERT INTO ticker (quoteVol, high24, baseVol, low24, HighBid, last, lowestAsk, percentChange, type, date) VALUES  (" + str(k["quoteVolume"]) + ", " + str(k["high"]) + ','  + str(k["volume"]) + ',' + str(k["quoteVolume"]) + ','  + str(k["low"]) + ','  + str(k["weightedAverage"])  + ','+ str(k["low"])  + ',' + "0" + ','  +"'all'"+  ",'"+timestamp +"')")

			print("done in " + str(time.time() - start))
			connection.commit()
			quit()
			"""
			cursor.execute("Select last from ticker  WHERE date >= ( CURDATE() - INTERVAL 200 DAY ) ORDER BY date DESC;") #Pull the last 200 days from DB
			bottom_tick_events200 = deque(cursor.fetchall())
			for i in bottom_tick_events200:
				SMA200.value += i[0]
			SMA200.value /= len(bottom_tick_events200) #Average that shit
			cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 50 DAY ) ORDER BY date DESC;") #Pull the last 200 days from DB
			bottom_tick_events50 = deque(cursor.fetchall())
			for i in bottom_tick_events50:
				SMA50.value += i[0] #repeate
			SMA50.value /= len(bottom_tick_events50)
			lenSMA50= len(bottom_tick_events50) #see how many events that took for each
			lenSMA200= len(bottom_tick_events200)


			while True : #And repeat forever
				time.sleep(3) #The number changes pretty slowly, and even 3 seconds produces a lot of duplicates

				ts = time.time()
				timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') #Convert to date-time
				query  = p.api_query("returnTicker") #Run the ticker event
				query = query[currency["currencyPair"]] #We only care about the current trading value, "USDT_ETH"
				top_tick_events += [trade_class.ticker(query, timestamp, currency["currencyPair"])] #Add it to a list of the past ticker events
				SMA50.value += (float(query["last"]) - bottom_tick_events50.popleft()[0]) / lenSMA50 #SMA that shit
				SMA200.value += (float(query["last"]) - bottom_tick_events200.popleft()[0]) / lenSMA200

				if len(top_tick_events) == 100: #When that list of events gets to 100, flush it and send it to MYSQL

					cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 200 DAY ) ORDER BY date DESC LIMIT 100") #Check my logic on this
					bottom_tick_events200 = deque(cursor.fetchall()) #Get the last 100 events. We cycle in 100 for the SMA math, and cycle out 1 event each iteration
																	# I think it'll work when we have a more consistent data set
					cursor.execute("Select last from ticker WHERE date >= ( CURDATE() - INTERVAL 50 DAY ) ORDER BY date DESC LIMIT 100")
					bottom_tick_events50 = deque(cursor.fetchall())

					print("Flushing to database") #write it all to sql
					for i in top_tick_events:
						cursor.execute(i.insert_sql());
						connection.commit()
					top_tick_events = []
		
	finally:
		connection.close()

#This tracks bids and asks to SQL. I kinda hate it
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
				OpenOrders[i[3]][i[0]] = trade_class.trades(i[0],i[1],i[2],i[3],i[4],i[5])
			sql = "INSERT INTO trades (amount, rate, type, creationdate) VALUES "#(%f, %f, %s, %s)
				
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
				"""	data = sql + "("+ str(i[1]) + ", " + str(i[0]) + ", 'USDT_ETH', '" + timestamp +"');"
					print(data)
					cursor.execute(data)
				connection.commit()
				quit()
				"""
	finally:
		connection.close()


"""
Get the current Orderbook of bids and asks
OpenOrders must be a manager.dict()
e is a multiprocessing.Event()
Cycling every half second for no good reason
"""
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
def init(O, S5, S2):
	global OrdersLock, SMA50Lock, SMA200Lock
	OrdersLock = O
	SMA50Lock = S5
	SMA200Lock = S2

def main():
	manager = multiprocessing.Manager() #This sets up a server that controls processing events
	e = multiprocessing.Event()

	OrdersLock = multiprocessing.Lock()
	SMA50Lock = multiprocessing.Lock()
	SMA200Lock = multiprocessing.Lock()
	pool = multiprocessing.Pool(initializer=init, initargs=(OrdersLock, SMA50Lock, SMA200Lock)) #Run the init function
	print("Setting up")
	SMA50 = manager.Value('d', 0.0)
	SMA200 = manager.Value('d', 0.0)

	OpenOrders = manager.dict()
	print("Spawning processes")
	OpenbookProcess = multiprocessing.Process(target=getOpenBook, args=(OpenOrders, e)) #Spawn some new processes
	OpenbookProcess.start()
	SMAProcess = multiprocessing.Process(target=SMA, args=(SMA50, SMA200))
	SMAProcess.start()
	print("Looping")
	while True:
		print("Main loop")
		time.sleep(0.75)
		e.wait() #Wait until a new orderbook is pulled

		for i in OpenOrders['bids']:
			if SMA200.value < float(i[0]):
				print(i[0], ": bid detected greater than 50 day average: ", SMA200.value)
main()
