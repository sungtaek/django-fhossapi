import MySQLdb
import logging
from pyexpat import model
from _csv import field_size_limit

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
	
	def select_by_model(self, models, conditions=None):
		q_sels = []
		q_tbls = []
		q_wheres = []
		q_values = []
		
		prev_model = None
		for model in models:
			q_sels.append(','.join(model._col_as_sel_names()))
			q_tbls.append(model.table)
			if prev_model:
				prev_rel_field = prev_model._get_rel_field(model)
				cur_rel_field = model._get_rel_field(prev_model)
				if prev_rel_field:
					left_name = prev_model._col_name(prev_rel_field)
					right_name = model._col_name(prev_rel_field.relation.peer_field)
				elif cur_rel_field:
					left_name = model._col_name(cur_rel_field)
					right_name = prev_model._col_name(cur_rel_field.relation.peer_field)
				else:
					raise ValueError('not found relation between %s and %s' % (prev_model.table, model.table))
				q_wheres.append('%s=%s' % (left_name, right_name))
			
		if conditions:
			for condition in conditions:
				if condition.field.type == Field.STRING and condition.value.find('%%') != -1:
					q_wheres.append('%s like %%s' % (condition.model._get_col_name(condition.field)))
				else:
					q_wheres.append('%s=%%s' % (condition.model._get_col_name(condition.field)))
				q_values.append(condition.value)
				
		q = 'select %s from %s' % (','.join(q_sels), ','.join(q_tbls))
		if len(q_wheres) > 0:
			q = q + ' where ' + ' and '.join(q_wheres)
		
		logger.debug('query -> ' + q)
		for value in q_values:
			logger.debug('values -> {}'.format(value))
		row_num = cls.db.execute(q, tuple(q_values))
		logger.debug('result <- %d rows' % (row_num))
		return row_num

class FieldRelation(object):
	def __init__(self, peer_model, peer_field):
		self.peer_model = peer_model
		self.peer_field = peer_field

class Field(object):
	STRING = 0
	INTEGER = 1

	def __init__(self, db_column, type, nullable=True, default=None, dictionable=True, relation=None):
		self.db_column = db_column
		self.type = type
		self.nullable = nullable
		self.default = default
		self.dictionable = dictionable
		self.relation = relation
		
class QueryCondition(object):
	def __init__(self, model, field, value):
		self.model = model
		self.field = field
		self.value = value

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
				raise ValueError('%s must be setted' % (key))
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
	def _get_rel_field(cls, peer_model):
		for field in cls._get_all_fields():
			if field.peer_model == peer_model:
				return field
		return None
			
	@classmethod
	def _col_name(cls, field):
		return cls.table + '.' + field.db_column
	
	@classmethod
	def _sel_name(cls, field):
		return cls.table + '_' + field.db_column

	@classmethod
	def _col_as_sel_names(cls):
		names = []
		for field in cls._get_all_fields().itervalues():
			names.append('%s as %s' % (cls._col_name(field), cls._sel_name(field)))
		return names

	@classmethod
	def _select(cls, one=False, **kwargs):
		objs = []
		conditions = []
		
		for key, value in kwargs.items():
			conditions.append(cls.condition(key, value))
			
		row_num = cls.db.select_by_model([cls], conditions)
		if row_num > 0:
			if one:
				row = cls.db.fetch_one()
				objs.append(cls.create_by_row(row))
			else:
				for rows in cls.db.fetch_all():
					objs.append(cls.create_by_row(row))
		return objs
	
	@classmethod
	def condition(cls, key, value):
		field = cls._get_field(key)
		if field:
			return QueryCondition(cls, field, value)
		else:
			raise ValueError('unknown field_key[%s]' % (key))

	@classmethod
	def create_by_row(cls, row):
		args = {}
		for key, val in cls._get_all_fields().iteritems():
			sel_name = cls._sel_name(key)
			if row.has_key(sel_name):
				args[key] = row[sel_name]
			elif row.has_key(val.db_column):
				args[key] = row[val.db_column]
		return cls(**args)

	@classmethod
	def get(cls, **kwargs):
		objs = cls._select(one=True, **kwargs)
		if len(objs) > 0:
			return objs[0]
		return None
	
	@classmethod
	def filter(cls, **kwargs):
		return cls._select(one=False, **kwargs)
	
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
		return value
				