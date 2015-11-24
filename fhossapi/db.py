import MySQLdb
import logging

# Create your models here.

logger = logging.getLogger('fhossapi')

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

	def execute(self, query, args=None):
		return self.cursor.execute(query, args)

	def fetch_all(self):
		return self.cursor.fetchall()

	def fetch_one(self):
		return self.cursor.fetchone()


class Field(object):
	STRING = 0
	INTEGER = 1

	def __init__(self, db_column, type, nullable=True, default=None, dictionable=True):
		self.db_column = db_column
		self.type = type
		self.nullable = nullable
		self.default = default
		self.dictionable = dictionable

class BaseModel(object):
	db = Database()
	
	'''
	Must override below variables
	table : table name
	fields : table columns info list (column_key, db_column_name, default_value, dict_yn)
	
	ex) mysql> desc user_tbl;
	+------------------------+--------------+------+-----+--------------+----------------+
	| Field                  | Type         | Null | Key | Default      | Extra          |
	+------------------------+--------------+------+-----+--------------+----------------+
	| id                     | int(11)      | NO   | PRI | NULL         | auto_increment |
	| name                   | varchar(255) | NO   | MUL |              |                |
	| address                | varchar(255) | YES  |     | NULL         |                |
	+------------------------+--------------+------+-----+--------------+----------------+

	table = 'user_tbl'
	identity = Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	user_name = Field('name', Field.STRING, nullable=False)
	address = Field('address', Field.STRING)
	'''
	table = None

	def __init__(self, **kwargs):
		for key, val in self._get_all_fields().iteritems():
			if kwargs.has_key(key):
				setattr(self, key, kwargs[key])
			elif val.default is not None:
				setattr(self, key, val.default)
			elif val.nullable is False:
				raise ValueError("%s must be setted" % (key))
			else:
				setattr(self, key, None)
			
	@classmethod
	def _get_field(cls, key):
		if key in cls.__dict__.keys():
			val = cls.__dict__[key]
			if isinstance(val, Field):
				return val
		return None
	
	@classmethod
	def _get_all_fields(cls):
		fields = {}
		for key in cls.__dict__.keys():
			val = cls.__dict__[key]
			if isinstance(val, Field):
				fields[key] = val
		return fields
			
	@classmethod
	def create_by_row(cls, row):
		args = {}
		for key, val in cls._get_all_fields().iteritems():
			sel_name = cls.sel_name(key)
			if row.has_key(sel_name):
				args[key] = row[sel_name]
			elif row.has_key(val.db_column):
				args[key] = row[val.db_column]
		return cls(**args)
	
	@classmethod
	def col_name(cls, key):
		val = cls._get_field(key)
		if val:
			return cls.table + '.' + val.db_column
		return None
	
	@classmethod
	def sel_name(cls, key):
		val = cls._get_field(key)
		if val:
			return cls.table + '_' + val.db_column
		return None

	@classmethod
	def col_as_sel_names(cls):
		names = []
		for key in cls._get_all_fields().iterkeys():
			names.append('%s as %s' % (cls.col_name(key), cls.sel_name(key)))
		return names

	@classmethod
	def get(cls, **kwargs):
		obj = None
		q_names = []
		q_values = []

		for name, value in kwargs.items():
			if cls._get_field(name):
				q_names.append('%s=%%s' % (name))
				q_values.append(value)
			else:
				raise ValueError("unknown field_key[%s]" % (name))

		q = 'select %s from %s' % (','.join(cls.col_as_sel_names()), cls.table)
		if len(q_names) > 0:
			q = q + ' where ' + ' and '.join(q_names)
		
		logger.debug('query -> %s' % (q))
		for value in q_values:
			logger.debug('values -> {}'.format(value))
		row_num = cls.db.execute(q, tuple(q_values))
		logger.debug('result <- %d rows' % (row_num))
		if row_num > 0:
			row = cls.db.fetch_one()
			obj = cls.create_by_row(row)
		
		return obj
	
	@classmethod
	def search(cls, **kwargs):
		objs = []
		q_names = []
		q_values = []
		
		for name, value in kwargs.items():
			field_val = cls._get_field(name)
			if field_val:
				if field_val.type == Field.STRING:
					q_name.append('%s like %%s' % (name))
					q_values.append('%' + value + '%')
				else:
					q_name.append('%s=%%s' % (name))
					q_values.append(value)
			else:
				raise ValueError("unknown field_key[%s]" % (name))

		q = 'select %s from %s' % (','.join(cls.col_as_sel_names()), cls.table)
		if len(q_names) > 0:
			q = q + ' where ' + ' and '.join(q_names)
		
		logger.debug('query -> %s' % (q))
		for value in q_values:
			logger.debug('values -> {}'.format(value))
		row_num = cls.db.execute(q, tuple(q_values))
		logger.debug('result <- %d rows' % (row_num))
		if row_num > 0:
			row = cls.db.fetch_one()
			while row:
				objs.append(cls.create_by_row(row))
				row = cls.db.fetch_one()
		
		return objs
	
	def save(self):
		'''
		must override this function
		'''
		return True

	def delete(self):
		'''
		must override this function
		'''
		return True
	
	def dict(self):
		value = {}
		for key, val in self._get_all_fields().iteritems():
			if val.dictionable and self.__dict__.has_key(key):
				value[key] = self.__dict__[key]
				
				