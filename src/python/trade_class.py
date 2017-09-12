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