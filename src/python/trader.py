#from Crypto.Cipher import AES
import api
#import base64
#import json
#import io
#import encrypt
import pymysql.cursors
import time
import datetime
import trade_class
import math

# Connect to the database
connection = pymysql.connect(host='localhost',
							 user='trader',
							 password='Immabigfatjuicypassword',
							 db='crypto')


def storeData(data, key):
	b = ""
	a = encrypt.encrypt(bytes(data), b, "qwertyuiop")
	print(a)

def loadData(key):
	with open('data.json', 'r') as fp:
		data = json.load(fp)

def load():
	alpb = 0
	alp[0]



def main():
	p = api.poloniex("A", "B")
	currency = {}
	currency["currencyPair"] = "USDT_ETH"
	OrderBook = {}
	OrderBook['bids'] = {}
	OrderBook['asks'] = {}
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

				query  = p.api_query("returnOrderBook", currency)
				
				ts = time.time()
				timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				OrderBookTemp = OrderBook.copy()
				NewTrades = []
				for i in query['bids']:
						for key, value in OrderBookTemp['bids'].items():
							if math.isclose(float(value.amount), float(i[1]), abs_tol=0.05) and math.isclose(float(value.rate), float(i[0]), abs_tol=0.05):
								del OrderBookTemp['bids'][key]
								query['bids'].remove(i)
								break

				for i in query['asks']:
						for key, value in OrderBookTemp['asks'].items():
							#pass
							if math.isclose(float(value.amount), float(i[1]), abs_tol=0.05) and math.isclose(float(value.rate), float(i[0]), abs_tol=0.05):
								print("removing", key)
								del OrderBookTemp['asks'][key]
								query['asks'].remove(i)
								break
				print("end checking")
				#remove old values from SQL and active list
				for key,value in OrderBookTemp['bids'].copy().items():
					del OrderBook['bids'][key]
					cursor.execute("update trades set selldate = '" + timestamp + "' where id = " + str(key))
				for key,value in OrderBookTemp['asks'].copy().items():
					del OrderBook['asks'][key]
					cursor.execute("update trades set selldate = '" + timestamp + "' where id = " + str(key))
				print("end pruning")
				#insert new values into SQL
				for i in query['bids']:
					data = sql + "("+ str(i[1]) + ", " + str(i[0]) + ", 'bids', '" + timestamp +"');"
					cursor.execute(data)
					connection.commit()
					cursor.execute("SELECT MAX(id) FROM trades;")
					newid = cursor.fetchone()[0]
					OrderBook["bids"][newid] = trade_class.trades(newid, i[1], i[0], "bids", timestamp, 0)
				for i in query['asks']:
					data = sql + "("+ str(i[1]) + ", " + str(i[0]) + ", 'asks', '" + timestamp +"');"
					cursor.execute(data)
					connection.commit()
					cursor.execute("SELECT MAX(id) FROM trades;")
					newid = int(cursor.fetchone()[0])
					OrderBook["asks"][newid] = trade_class.trades(newid, i[1], i[0], "bids", timestamp, 0)
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
main()
#[{data: {rate: '0.00300888', type: 'bid', amount: '3.32349029'},type: 'orderBookModify'}]

#[{data: {rate: '0.00311164', type: 'ask' },type: 'orderBookRemove'}]