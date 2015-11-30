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
		if request.GET.has_key('offset') and request.GET['offset'] > 0:
			offset = request.GET['offset']
		if request.GET.has_key('limit') and request.GET['limit'] > 0:
			if request.GET['limit'] > 30:
				limit = 30
			else:
				limit = request.GET['limit']
		
		imsus = Imsu.objects.prefetch_related('impis__impus__service_profile').filter(**filters).order_by('name')[offset:limit]
		users = []
		for imsu in imsus:
			users.append(get_user_dic(imsu))
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
			imsu = Imsu.objects.prefetch_related('impis__impus__service_profile').get(name=name)
		except:
			raise NotFound('User[%s] not found.' % (name))
		
		resp['user'] = get_user_dict(imsu)
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
	"""
	# permission_classes = (IsAuthenticated,)

	def get(self, request):
		resp = {}
		return Response(resp)


class ServiceDetailView(APIView):
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

