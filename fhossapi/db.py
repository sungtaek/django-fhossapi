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

	def execute(self, query):
		return self.cursor.execute(query)

	def execute_pstmt(self, pstmt, *args):
		return self.cursor.execute(pstmt, args)

	def fetch_all(self):
		return self.cursor.fetchall()

	def fetch_one(self):
		return self.cursor.fetchone()

