"""views.py"""

import datetime
import json

from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required

from .models import User, Investor, Stock, Portfolio, Stock_Owned, Portfolio_Day
from predict_my_money.utils import stockAPI, portfolioAPI
from predict_my_money.computations.recommender_interface import recommend_diverse_portfolio, recommend_high_return_portfolio, recommend_random_portfolio, \
	recommend_interfacer

sapi = stockAPI()
papi = portfolioAPI()

def error(request):
	return HttpResponse("An Error occured.")

# Create your views here.

def index(request):
	if request.user:
		return HttpResponseRedirect(reverse('predictor:home'))
	else:
		return HttpResponseRedirect(reverse('predictor:login'))


@login_required
def home(request):
	try:
		user = User.objects.get(pk=request.user.id)
	except User.DoesNotExist:
		raise Http404("User does not exist")

	investor = Investor.objects.get(user=request.user.id)
	portfolios = Portfolio.objects.filter(investor=investor)

	return render(request, 'predictor/home.html', {
		'investor': investor,
		'portfolios': portfolios,
		'user': user
	})


def portfolio_detail(request, portfolio_id):
	portfolio = papi.getPortfolio(portfolio_id)
	if not portfolio:
		return render(request, 'predictor/error.html', {
			'error_message': "Portfolio doesn't exist.",
		})
	return render(request, 'predictor/portfolio_detail.html', {
		'portfolio' : portfolio
	})


@require_GET
def portfolio_compare(request):
	return render(request, 'predictor/portfolio_compare.html', {})

@require_GET
def stock_detail(request, stock_ticker):
	return render(request, 'predictor/stock.html', {
		'stock_ticker': stock_ticker,
	})

@require_GET
def create_portfolio(request):
	return render(request, 'predictor/new_portfolio.html')


def portfolio_detail_json(request, portfolio_id):
	api = portfolioAPI()
	portfolio = api.getPortfolio(portfolio_id)
	storage = {}
	investor = portfolio.investor.user.first_name + " " + portfolio.investor.user.last_name
	name = portfolio.portfolio_name
	diversity = portfolio.current_diversity
	value = portfolio.current_value
	days = Portfolio_Day.objects.order_by('day').filter(portfolio=portfolio)
	daysDict = {}
	for day in days:
		daysDict[day.day.__str__()] = {'value':day.value, 'diversity':day.diversity}
	storage['investor'] = investor
	storage['name'] = name
	storage['diversity'] = diversity
	storage['value'] = value
	storage['days'] = daysDict
	return HttpResponse(json.dumps(storage), content_type="application/json")

