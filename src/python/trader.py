from Crypto.Cipher import AES
import api
import base64
import json
import io
import encrypt
import sqlite3
def storeData(data, key):
	b = ""
	a = encrypt.encrypt(bytes(data), b, "qwertyuiop")
	print(a)

def loadData(key):
	with open('data.json', 'r') as fp:
		data = json.load(fp)


def main2():
	#trader = poloniex(data["key"], data["pass"])

	key = "ImmaBiglongJuicyPasswordYaBabyes"
	data = {"bought": "226.49", "sold" : "250", "aggression" : "1.0", "key" : "key", "pass" : "pass"}
	storeData(data, key)
	loadData(key)

def main():
	conn = sqlite3.connect("trade.db")
	c = conn.cursor()
	data  = {}
	with open('history.json', 'r') as fp:
		data = json.load(fp)
	for k in data:
		c.execute("INSERT INTO ticker (currency, last, lowest, highest, change, baseeVol, quoteVol, date) VALUES ('USDT_ETH', " + str(k["open"]) + ','  + str(k["low"]) + ',' + str(k["high"]) + ',' + "0" + ',' + str(k["volume"]) + ',' + str(k["quoteVolume"]) + ',' + str(k["date"]) +")")
	
	conn.commit()
	print ("Records created successfully")
	conn.close()
main()