import MySQLdb

def singleton(cls):
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance

@singleton
class Database(object):
	def __init__(self):
		self.db = MySQLdb.connect('localhost','hss','hss','hss_db')
		self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

	def execute(self, *args):
		return self.cursor.execute(*args)

	def fetch_all(self):
		return self.cursor.fetchall()

	def fetch_one(self):
		return self.cursor.fetchone()

