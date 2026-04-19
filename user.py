from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from db import *

user_db = UserDB()

class User(UserMixin):
	def __init__(self, id):
		self.id = id
		self.username = id 
		self.role = user_db.get_user_by_username(self.username)[3]

	def is_admin(self):
		return self.role=="admin"

	@staticmethod
	def get(user_id):
		if user_db.get_user_by_username(user_id):
			return User(user_id)
		else:
			return None

