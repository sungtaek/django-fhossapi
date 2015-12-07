from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
import logging
import json
from .models import *

# Create your views here.

logger = logging.getLogger('fhossapi')


'''
def get_user_dict(imsu):
	user_dic = model_to_dict(imsu)
	user_dic['impi'] = []
	for impi in imsu.impis.all():
		impi_dic = model_to_dict(impi)
		impi_dic['impu'] = []
		for impu in impi.impus.all():
			impu_dic = model_to_dict(impu)
			impu_dic['service_profile'] = impu.service_profile.name
			impi_dic['impu'].append(impu_dic)
		user_dic['impi'].append(impi_dic)
	return user_dic
'''

def index(request):
	return HttpResponseRedirect("/hss.api/docs")

class AuthToken(APIView):
	"""
	Get auth token
	---
	GET:
		parameters:
			- name: username
			  description: username
			  required: true
			  type: string
			  paramType: query
			- name: password
			  description: password
			  required: true
			  type: string
			  paramType: query
	"""

	def get(self, request):
		username = request.query_params.get('username')
		password = request.query_params.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if user:
				if not user.is_active:
					raise PermissionDenied('User account is disabled.')
			else:
				raise NotAuthenticated('Unable to log in with provided credentials.')
		else:
			raise ValidationError('Must include "username" and "password" parameters.')

		token = Token.objects.get(user=user)
		resp = {}
		resp['token'] = token.key
#resp['created'] = created
		return Response(resp)

class UserSearchView(APIView):
	"""
	search subscriber
	---
	GET:
		parameters:
			- name: name
			  description: user name
			  required: false
			  type: string
			  paramType: query
			- name: impi
			  description: user impi identity
			  required: false
			  type: string
			  paramType: query
			- name: impu
			  description: user impu identity
			  required: false
			  type: string
			  paramType: query
			- name: regi
			  description: register status
			  required: false
			  type: boolean
			  default: false
			  paramType: query
			- name: detail
			  description: display detail info
			  required: false
			  type: boolean
			  default: false
			  paramType: query
			- name: offset
			  description: query offset (default:0)
			  required: false
			  type: integer
			  default: 0
			  paramType: query
			- name: limit
			  description: query limit (default:10, max:30)
			  required: false
			  type: integer
			  default: 10
			  paramType: query
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
		
		filters = {}
		detail = False
		offset = 0
		limit = 10
		if request.GET.has_key('name'):
			filters['name__icontains'] = request.GET['name']
		if request.GET.has_key('impi'):
			filters['impis__identity__icontains'] = request.GET['impi']
		if request.GET.has_key('impu'):
			filters['impis__impus__identity__icontains'] = request.GET['impu']
		if request.GET.has_key('regi') and request.GET['regi']:
			filters['impis__impus__user_status'] = 1
		if request.GET.has_key('detail') and request.GET['detail'] == 'true':
			detail = True
		if request.GET.has_key('offset') and int(request.GET['offset']) > 0:
			offset = int(request.GET['offset'])
		if request.GET.has_key('limit') and int(request.GET['limit']) > 0:
			if int(request.GET['limit']) > 30:
				limit = 30
			else:
				limit = int(request.GET['limit'])
		

		logger.debug('filter -> %s' % (json.dumps(filters)))
		logger.debug('detail -> %s' % (detail))
		logger.debug('offset -> %d' % (offset))
		logger.debug('limit -> %d' % (limit))
		qs = Imsu.objects
		qs = qs.select_related('capa_set')
		qs = qs.select_related('pref_scscf')
		qs = qs.prefetch_related('impis__impus__service_profile')
		imsus = qs.filter(**filters).order_by('name')[offset:limit]
		users = []
		for imsu in imsus:
			users.append(imsu.dict(detail))
		resp['count'] = len(users)
		resp['offset'] = offset
		resp['limit'] = limit
		resp['user'] = users
		return Response(resp)

class UserDetailView(APIView):
	"""
	manage subscriber
	---
	GET:
		parameters:
			- name: name
			  description: user name
			  required: true
			  type: string
			  paramType: path
	POST:
		parameters:
			- name: name
			  description: user name
			  required: true
			  type: string
			  paramType: path
			- name: user_info
			  description: user info
			  required: true
			  type: json
			  paramType: body
	PUT:
		parameters:
			- name: name
			  description: user name
			  required: true
			  type: string
			  paramType: path
			- name: user_info
			  description: user info
			  required: true
			  type: json
			  paramType: body
	DELETE:
		parameters:
			- name: name 
			  description: user name
			  required: true
			  type: string
			  paramType: path
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request, name):
		resp = {}
		imsu = None
		try:
			qs = Imsu.objects
			qs = qs.select_related('capa_set')
			qs = qs.select_related('pref_scscf')
			qs = qs.prefetch_related('impis__impus__service_profile')
			imsu = qs.get(name=name)
		except:
			raise NotFound('User[%s] not found.' % (name))
		
		resp['user'] = imsu.dict()
		return Response(resp)

	def post(self, request, name):
		resp = {}
		return Response(resp)

	def put(self, request, name):
		resp = {}
		return Response(resp)

	def delete(self, request, name):
		resp = {}
		return Response(resp)

class ServiceSearchView(APIView):
	"""
	get list of service
	---
	GET:
		parameters:
			- name: name
			  description: service_profile name
			  required: false
			  type: string
			  paramType: query
			- name: as
			  description: aplication_server name
			  required: false
			  type: string
			  paramType: query
			- name: detail
			  description: display detail info
			  required: false
			  type: boolean
			  default: false
			  paramType: query
			- name: offset
			  description: query offset (default:0)
			  required: false
			  type: integer
			  default: 0
			  paramType: query
			- name: limit
			  description: query limit (default:10, max:30)
			  required: false
			  type: integer
			  default: 10
			  paramType: query
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
		
		filters = {}
		detail = False
		offset = 0
		limit = 10
		if request.GET.has_key('name'):
			filters['name__icontains'] = request.GET['name']
		if request.GET.has_key('as'):
			filters['ifcs__application_server__name__icontains'] = request.GET['as']
		if request.GET.has_key('detail') and request.GET['detail'] == 'true':
			detail = True
		if request.GET.has_key('offset') and int(request.GET['offset']) > 0:
			offset = int(request.GET['offset'])
		if request.GET.has_key('limit') and int(request.GET['limit']) > 0:
			if int(request.GET['limit']) > 30:
				limit = 30
			else:
				limit = int(request.GET['limit'])
				
		logger.debug('filter -> %s' % (json.dumps(filters)))
		logger.debug('detail -> %s' % (detail))
		logger.debug('offset -> %d' % (offset))
		logger.debug('limit -> %d' % (limit))
		qs = ServiceProfile.objects
		qs = qs.prefetch_related('ifcs__application_server')
		qs = qs.prefetch_related('ifcs__trigger_point__spts')
		sps = qs.filter(**filters).order_by('name')[offset:limit]
		services = []
		for sp in sps:
			services.append(sp.dict(detail))
		resp['count'] = len(services)
		resp['offset'] = offset
		resp['limit'] = limit
		resp['service'] = services
		return Response(resp)


class ServiceDetailView(APIView):
	"""
	manage service 
	---
	GET:
		parameters:
			- name: name
			  description: service_profile name
			  required: true
			  type: string
			  paramType: path
	POST:
		parameters:
			- name: name
			  description: service_profile name
			  required: true
			  type: string
			  paramType: path
			- name: profile_info
			  description: service_profile info
			  required: true
			  type: json
			  paramType: body
	PUT:
		parameters:
			- name: name
			  description: service_profile name
			  required: true
			  type: string
			  paramType: path
			- name: profile_info
			  description: service_profile info
			  required: true
			  type: json
			  paramType: body
	DELETE:
		parameters:
			- name: name
			  description: service_profile name
			  required: true
			  type: string
			  paramType: path
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request, name):
		resp = {}
		sp = None
		try:
			qs = ServiceProfile.objects
			qs = qs.prefetch_related('ifcs__application_server')
			qs = qs.prefetch_related('ifcs__trigger_point__spts')
			sp = qs.get(name=name)
		except:
			raise NotFound('Service[%s] not found.' % (name))
		
		resp['service'] = sp.dict()
		return Response(resp)

	def post(self, request, name):
		resp = {}
		return Response(resp)

	def put(self, request, name):
		resp = {}
		return Response(resp)

	def delete(self, request, name):
		resp = {}
		return Response(resp)

