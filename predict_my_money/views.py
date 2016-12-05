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


@require_GET
def portfolio(request, pid):
	portfolio = papi.getPortfolio(pid)
	if not portfolio:
		return render(request, 'predictor/error.html', {
			"portfolio": portfolio,
			'error_message': "Portfolio doesn't exist.",
		})

	stocks = papi.getStocksOwned(pid)

	return render(request, 'predictor/portfolio_detail.html', {
		'portfolio' : portfolio,
		'stocks': stocks,
	})


@require_GET
def portfolio_compare(request, pid0, pid1):
	print(pid0, pid1)

	p0 = papi.getPortfolio(pid0)
	p1 = papi.getPortfolio(pid1)

	if not p0 or not p1:
		return render(request, 'predictor/error.html', {
			'error_message': "Portfolio doesn't exist.",
		})

	stocks0 = papi.getStocksOwned(pid0)
	stocks1 = papi.getStocksOwned(pid1)

	return render(request, 'predictor/portfolio_compare.html', {
		"portfolio1": p0,
		"stocks1": stocks0,
		"portfolio2": p1,
		"stocks2": stocks1,
	})

@require_GET
def stock_detail(request, ticker):
	stock = sapi.getStock(ticker)
	if not stock:
		return render(request, 'predictor/error.html', {
			'error_message': "Stock doesn't exist."
		})

	return render(request, 'predictor/stock.html', {
		'stock': stock,
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

