from django.db import models
from .db import BaseModel, Field
import logging

# Create your models here.

logger = logging.getLogger('fhossapi')

class User(BaseModel):
	table = 'imsu'
	id			= Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	name		= Field('name', Field.STRING, nullable=False)
	scscf_name	= Field('scscf_name', Field.STRING)
	diameter_name= Field('diameter_name', Field.STRING)
	capa_set	= Field('id_capabilities_set', Field.INTEGER)
	pref_scscf	= Field('id_preferred_scscf_set', Field.INTEGER)

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		self.impi = None
		self.impu = None

	def dict(self):
		value = super(User, self).dict()
		if self.impi:
			value['impi'] = self.impi.dict()
		if self.impu:
			value['impu'] = self.impu.dict()
		return value

	@classmethod
	def get_with_impi_impu(cls, user_args=None, impi_args=None, impu_args=None):
		user = None
		conditions = []
		
		if user_args:
			for key, value in user_args.iteritmes():
				conditions.append(User.condition(key, value))
				
		if impi_args:
			for key, value in impi_args.iteritmes():
				conditions.append(Impi.condition(key, value))

		if impu_args:
			for key, value in impu_args.iteritmes():
				conditions.append(Impu.condition(key, value))
				
		row_num = cls.db.select_by_model([User,Impi,ImpiImpu,Impu], conditions)
		if row_num > 0:
			row = cls.db.fetch_one()
			user = User.create_by_row(row)
			user.impi = Impi.create_by_row(row)
			user.impu = Impu.create_by_row(row)
		return user
	
	@classmethod
	def filter_with_impi_impu(cls, user_args=None, impi_args=None, impu_args=None):
		users = []
		conditions = []
		
		if user_args:
			for key, value in user_args.iteritmes():
				conditions.append(User.condition(key, value))
				
		if impi_args:
			for key, value in impi_args.iteritmes():
				conditions.append(Impi.condition(key, value))

		if impu_args:
			for key, value in impu_args.iteritmes():
				conditions.append(Impu.condition(key, value))
				
		row_num = cls.db.select_by_model([User,Impi,ImpiImpu,Impu], conditions)
		if row_num > 0:
			for row in cls.db.fetch_all():
				user = User.create_by_row(row)
				user.impi = Impi.create_by_row(row)
				user.impu = Impu.create_by_row(row)
				users.append(user)
		return users

class Impi(BaseModel):
	table		= 'impi'

	id			= Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	id_imsu		= Field('id_imsu', Field.INTEGER, default=-1, dictionable=False, relation=FieldRelation(User, User.id))
	identity	= Field('identity', Field.STRING, nullable=False)
	secret_key	= Field('k', Field.STRING, nullable=False)
	avail_auth	= Field('auth_scheme', Field.INTEGER, nullable=False, default=129)
	def_auth	= Field('default_auth_scheme', Field.INTEGER, nullable=False, default=128)
	amf			= Field('amf', Field.STRING, nullable=False, default='0000')
	op			= Field('op', Field.STRING, nullable=False, default='00000000000000000000000000000000')
	sgn			= Field('sgn', Field.STRING, nullable=False, default='000000000000')
	early_ims_ip= Field('ip', Field.STRING, nullable=False, default='')
	dsl_line_id	= Field('line_identifier', Field.STRING, nullable=False, default='')
	
class ImpiImpu(BaseModel):
	table		= 'impi_impu'
	
	id			= Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	id_impi		= Field('id_impi', Field.INTEGER, nullable=False, default=0, dictionable=False, relation=FieldRelation(Impi, Impi.id))
	id_impu		= Field('id_impu', Field.INTEGER, nullable=False, default=0, dictionable=False, relation=FieldRelation(Impu, Impu.id))
	user_status	= Field('user_state', Field.INTEGER, nullable=False, default=0, dictionable=False)

class Impu(BaseModel):
	table		= 'impu'
	id			= Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	identity	= Field('identity', Field.STRING, nullable=False)
	impu_type	= Field('type', Field.INTEGER, nullable=False, default=0)
	barring		= Field('barring', Field.INTEGER, nullable=False, default=0)
	user_status	= Field('user_state', Field.INTEGER, nullable=False, default=0)
	service_profile	= Field('id_sp', Field.INTEGER, nullable=False)
	id_implicit_set	= Field('id_implict_set', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	charging_info_set= Field('id_charging_info', Field.INTEGER, default=-1)
	wildcard_psi	= Field('wildcard_psi', Field.STRING, nullable=False, default='')
	display_name	= Field('display_name', Field.STRING, nullable=False, default='')
	psi_activation	= Field('psi_activation', Field.INTEGER, nullable=False, default=0)
	can_register	= Field('can_register', Field.INTEGER, nullable=False, default=0)

class ImpuVisitedNetwork(BaseModel):
	table		= 'impu_visited_network'
	id			= Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	id_impi		= Field('id_impu', Field.INTEGER, nullable=False, default=0, dictionable=False, relation=FieldRelation(Impu, Impu.id))
	id_impu		= Field('id_visited_network', Field.INTEGER, nullable=False, default=0, dictionable=False, relation=FieldRelation(VisitedNetwork, VisitedNetwork.id))
	
class VisitedNetwork(BaseModel):
	table		= 'visited_network'
	id			= Field('id', Field.INTEGER, nullable=False, default=-1, dictionable=False)
	identity	= Field('identity', Field.STRING, nullable=False)
