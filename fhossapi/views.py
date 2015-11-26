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

class UserListView(APIView):
	"""
	get list of subscriber
	---
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
		return Response(resp)

class UserAddView(APIView):
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
	# permission_classes = (IsAuthenticated,)

	def post(self, request):
		resp = {}
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
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
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
		try:
			imsu = Imsu.objects.prefetch_related('impis').get(name=name)
		except e:
			raise NotFound('User[%s] not found.' % (name))
		user = model_to_dict(imsu)
		user['impi'] = []
		for impi in imsu.impis.all():
			impi_dic = model_to_dict(impi)
			impi_dic['impu'] = []
			for impu in impi.impus.all():
				impi_dic['impu'].append(model_to_dict(impu))
			user['impi'].append(impi_dic)

		return Response(user)

	def put(self, request, name):
		resp = {}
		return Response(resp)

	def delete(self, request, name):
		resp = {}
		return Response(resp)

class ServiceList(APIView):
	"""
	get list of service
	---
	"""
	# permission_classes = (IsAuthenticated,)

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
	# permission_classes = (IsAuthenticated,)

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
	# permission_classes = (IsAuthenticated,)

	def get(self, request, identity):
		resp = {}
		return Response(resp)

	def put(self, request, identity):
		resp = {}
		return Response(resp)

	def delete(self, request, identity):
		resp = {}
		return Response(resp)

