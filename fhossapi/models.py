from django.db import models
from .db import Database

# Create your models here.

class User(object):
	db = Database()

	impu = None
	impu_type = None
	barring = None
	user_state = None
	service_id = None
	impi = None
	password = None
	default_auth = None
