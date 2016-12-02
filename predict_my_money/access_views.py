"""access_views.py"""

import datetime
import json

from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from predict_my_money.utils import stockAPI, portfolioAPI, stockDayDatabaseInterface
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest

from .models import User, Investor

# Create your views here.

def register(request):
	if request.method == "GET":
		template = loader.get_template('access/register.html')
		context = {}
		return HttpResponse(template.render(context, request))
	elif request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		name = request.POST['name']

		user = User.objects.create_user(username, email, password)
		# user.first_name, user.last_name = name.split()
		user.save()
		investor = Investor()
		investor.user = user
		investor.save()
		djangoLogin(request, user)
		return HttpResponseRedirect(reverse('predictor:home'))
	else:
		return HttpResponseBadRequest("Invalid method.")


def login(request):
	if request.method == "GET":
		template = loader.get_template('access/login.html')
		context = {}
		return HttpResponse(template.render(context, request))
	elif request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user:
			return render(request, 'predictor/error.html', {
				'error_message': "Invalid Login.",
			})

		login(request, user)
		return HttpResponseRedirect(reverse('predictor'))
	else:
		return HttpResponseBadRequest("Invalid method.")


def logout(request):
	djangoLogout(request)
	return HttpResponse('You have successfully signed out.')

	