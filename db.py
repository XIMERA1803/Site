import sqlite3

class DataBase:
	def __init__(self, path="db.db"):
		self.conn = sqlite3.connect(path, check_same_thread=False)
		self.cur = self.conn.cursor()

	def select_all(self):
		result = self.cur.execute("SELECT * FROM projects").fetchall()
		return result

