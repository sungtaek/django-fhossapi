from django.db import models
from .db import Database
import logging

# Create your models here.

logger = logging.getLogger('fhossapi')

class BaseModel(object):
	db = Database()
	table = None

	@classmethod
	def get(cls, **kwargs):
		obj = None

		query = 'select * from %s' % (cls.table)
		first = True
		for name, value in kwargs.items():
			if first:
				query = '%s where' % (query)
			else :
				query = '%s and' % (query)
			first = False
			
			logger.debug('param %s=%s(%s)' % (name, value, type(value)))
			if type(value) is str or type(value) is unicode:
				query = '%s %s=\'%s\'' % (query, name, value)
			else:
				query = '%s %s=%s' % (query, name, value)
		
		logger.debug('query -> %s' % (query))
		row_num = cls.db.execute(query)
		logger.debug('rows <- %d' % (row_num))
		if row_num > 0:
			row = cls.db.fetch_one()
			obj = cls._init_by_row(row)
		
		return obj
	
	@classmethod
	def _init_by_row(cls, row):
		'''
		must override this function
		'''
		return cls()

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

	
class User(BaseModel):
	table = 'imsu'
	
	def __init__(self, name, id=-1, capa_set=-1, pref_scscf='', scscf_name='', diameter_name=''):
		self.id = id
		self.name = name
		self.capa_set = capa_set
		self.pref_scscf = pref_scscf
		self.scscf_name = scscf_name
		self.diameter_name = diameter_name
		self.impi = None
		self.impu = None
		
	def __dict__(self):
		val = {}
		val['name'] = self.name
		val['capa_set'] = self.capa_set
		val['pref_scscf'] = self.pref_scscf
		val['scscf_name'] = self.scscf_name
		val['diameter_name'] = self.diameter_name
		if impi:
			val['impi'] = self.impi.__dict__()
		if impu:
			val['impu'] = self.impu.__dict__()
		return val

	@classmethod
	def _init_by_row(cls, row):
		return cls(name = row['name']
				, capa_set = row['id_capabilities_set']
				, pref_scscf = row['id_preferred_scscf_set']
				, scscf_name = row['scscf_name']
				, diameter_name= row['diameter_name'])

			
	@classmethod
	def get_by_impi(cls, **kwargs):
		user = None
		impi = Impi.gets(**kwargs)
		if impi and impi.id_imsu >= 0:
			user = User.get(id=impi.id_imsu)
			if user:
				user.impi = impi
		return user
	
	@classmethod
	def get_by_impu(cls, **kwargs):
		user = None
		impu = Impu.get(**kwargs)
		if impu:
			impi = Impi.get_by_impu(impu.id)
			if impi and impi.id_imsu>= 0:
				user = User.get(id=impi.id_imsu)
				user.impi = impi
				user.impu = impu
		return user
			

class Impi(BaseModel):
	table = 'impi'
	
	def __init__(self, identity, secret_key, id=-1
				, id_imsu = -1, avail_auth = 129, def_auth = 128):
		self.id = id
		self.id_imsu = id_imsu
		self.identity = identity
		self.secret_key = secret_key
		self.avail_auth = avail_auth
		self.def_auth = def_auth
		self.amf = '0000'
		self.op = '00000000000000000000000000000000'
		self.sgn = '000000000000'
		self.early_ims_ip = ''
		self.dsl_line_identifier = ''

	def __dict__(self):
		val = {}
		val['identity'] = self.identity
		val['secret_key'] = self.secret_key
		val['avail_auth'] = self.avail_auth
		val['def_auth'] = self.def_auth
		val['amf'] = self.amf
		val['op'] = self.op
		val['sgn'] = self.sgn
		val['early_ims_ip'] = self.early_ims_ip
		val['dsl_line_identifier'] = self.dsl_line_identifier
		return val
		
	@classmethod	
	def _init_by_row(cls, row):
		return cls(id = row['id']
				, id_imsu = row['id_imsu']
				, identity = row['identity']
				, secret_key = row['k']
				, avail_auth = row['auth_scheme']
				, def_auth = row['default_auth_scheme'])
		
	@classmethod
	def get_by_impu(cls, impu_id):
		impi = None
		query = 'select id_impi from impi_impu where id_impu=\'%s\'' % (impu_id)
		row_num = cls.db.execute(query)
		if row_num > 0:
			row = cls.db.fetch_one()
			impi = Impi.get(id=row['id_impi'])
		return impi
	
class Impu(BaseModel):
	table = 'impu'
	
	def __init__(self, identity, service_profile, id=-1
				, user_status=0, impu_type=0, barring=False
				, charging_info_set=-1, can_register=True
				, wildcard_psi='', psi_activation=False
				, display_name='', visited_networks=[]):
		self.id = id
		self.identity = identity
		self.service_profile = service_profile
		self.user_status = user_status
		self.impu_type = impu_type 
		self.barring = barring
		self.charging_info_set = charging_info_set
		self.can_register = can_register
		self.wildcard_psi = wildcard_psi
		self.psi_activation = psi_activation
		self.display_name = display_name
		self.visited_networks = visited_networks
		
	def __dict__(self):
		val = {}
		val['identity'] = self.identity
		val['service_profile'] = self.service_profile
		val['user_status'] = self.user_status
		val['impu_type'] = self.impu_type
		val['barring'] = self.barring
		val['charging_info_set'] = self.charging_info_set
		val['wildcard_psi'] = self.wildcard_psi
		val['psi_acrivation'] = self.psi_activation
		val['display_name'] = self.display_name
		val['visited_networks'] = self.visited_networks
		return val
		
	@classmethod
	def _init_by_row(cls, row):
		return cls(id = row['id']
				, identity = row['identity']
				, service_profile = row['id_sp']
				, user_status = row['user_state']
				, impu_type = row['type']
				, barring = (row['barring'] == 1)
				, charging_info_set = row['id_charging_info']
				, can_register = (row['can_register'] == 1)
				, wildcard_psi = row['wildcard_psi']
				, psi_activation = (row['psi_activation'] == 1)
				, display_name = row['display_name'])
