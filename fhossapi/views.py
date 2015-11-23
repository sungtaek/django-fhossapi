from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
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

def get_authname(auth):
	if auth == 1:
		return 'Digest-AKAv1-MD5'
	elif auth == 2:
		return 'Digest-AKAv2-MD5'
	elif auth == 4:
		return 'Digest-MD5'
	elif auth == 8:
		return 'Digest'
	elif auth == 16:
		return 'HTTP-Digest-MD5'
	elif auth == 32:
		return 'Early-IMS-Security'
	elif auth == 64:
		return 'NASS-Bundled'
	elif auth == 128:
		return 'SIP-Digest'
	else:
		return 'Unknown'

def get_impu_by_row(row, detail=False):
	if row['barring'] == 0:
		barring = False
	else:
		barring = True

	if row['type'] == 0:
		impu_type = 'Public User Identity'
	elif row['type'] == 1:
		impu_type = 'Distinct PSI'
	elif row['type'] == 2:
		impu_type = 'Wildcarded PSI'
	else:
		impu_type = 'Unknown'

	if row['user_state'] == 0:
		user_state = 'Not Registered'
	elif row['user_state'] == 1:
		user_state = 'Registered'
	elif row['user_state'] == 2:
		user_state = 'Unregistered'
	elif row['user_state'] == 3:
		user_state = 'Auth-Pending'
	else:
		user_state = 'Unknown'

	if detail:
		return {
			'identity': row['identity'],
			'type': impu_type,
			'barring': barring,
			'user_state': user_state,
			'service_id': row['id_sp']
		}
	else:
		return {
			'identity': row['identity'],
			'user_state': user_state,
		}

def get_impi_by_row(row):

	if row['default_auth_scheme'] == 1:
		default_auth = 'Digest-AKAv1-MD5'
	elif row['default_auth_scheme'] == 2:
		default_auth = 'Digest-AKAv2-MD5'
	elif row['default_auth_scheme'] == 4:
		default_auth = 'Digest-MD5'
	elif row['default_auth_scheme'] == 8:
		default_auth = 'Digest'
	elif row['default_auth_scheme'] == 16:
		default_auth = 'HTTP-Digest-MD5'
	elif row['default_auth_scheme'] == 32:
		default_auth = 'Early-IMS-Security'
	elif row['default_auth_scheme'] == 64:
		default_auth = 'NASS-Bundled'
	elif row['default_auth_scheme'] == 128:
		default_auth = 'SIP-Digest'
	else:
		default_auth = 'Unknown'

	return {
		'identity': row['identity'],
		'password': row['k'],
		'default_auth': default_auth
	}

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

class UserList(APIView):
	"""
	get list of subscriber
	---
	"""
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
		return Response(resp)

class UserAdd(APIView):
	"""
	manage subscriber
	---
	POST:
		parameters:
			- name: user_info
			  description: user info
			  required: true
			  type: json
			  paramType: body
	"""
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		resp = {}
		return Response(resp)

class User(APIView):
	"""
	manage subscriber
	---
	GET:
		parameters:
			- name: identity
			  description: impu identity
			  required: true
			  type: string
			  paramType: path
	PUT:
		parameters:
			- name: identity
			  description: impu identity
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
			- name: identity
			  description: impu identity
			  required: true
			  type: string
			  paramType: path
	"""
	permission_classes = (IsAuthenticated,)

	def get(self, request, identity):
		user = User.get_by_impu(identity=identity)
		return Response(user)

	def put(self, request, identity):
		resp = {}
		return Response(resp)

	def delete(self, request, identity):
		resp = {}
		return Response(resp)

class ServiceList(APIView):
	"""
	get list of service
	---
	"""
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
		return Response(resp)

class ServiceAdd(APIView):
	"""
	manage service 
	---
	POST:
		parameters:
			- name: user_info
			  description: user info
			  required: true
			  type: json
			  paramType: body
	"""
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		resp = {}
		return Response(resp)

class Service(APIView):
	"""
	manage service 
	---
	GET:
		parameters:
			- name: identity
			  description: impu identity
			  required: true
			  type: string
			  paramType: path
	PUT:
		parameters:
			- name: identity
			  description: impu identity
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
			- name: identity
			  description: impu identity
			  required: true
			  type: string
			  paramType: path
	"""
	permission_classes = (IsAuthenticated,)

	def get(self, request, identity):
		resp = {}
		return Response(resp)

	def put(self, request, identity):
		resp = {}
		return Response(resp)

	def delete(self, request, identity):
		resp = {}
		return Response(resp)

