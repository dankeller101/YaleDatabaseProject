"""views.py"""

import datetime
import json

from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from predict_my_money.utils import stockAPI, portfolioAPI, stockDayDatabaseInterface
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .models import User, Investor, Stock, Portfolio, Stock_Owned, Portfolio_Day
from predict_my_money.computations.recommender_interface import recommend_diverse_portfolio, recommend_high_return_portfolio, recommend_random_portfolio, \
	recommend_interfacer

# Create your views here.

def index(request):
	if request.user:
		return HttpResponseRedirect(reverse('predictor:home'))
	else:
		return HttpResponseRedirect(reverse('predictor:login'))


def home(request):
	print request.user
	try:
		user = User.objects.get(pk=request.user.id)
	except User.DoesNotExist:
		raise Http404("User does not exist")
	else:
		investor = Investor.objects.get(user=request.user.id)
		return render(request, 'predictor/home.html', {'investor': investor, 'user': user})


def portfolio_detail(request, portfolio_id):
	portAPI = portfolioAPI()
	portfolio = portAPI.getPortfolio(portfolio_id)
	if portfolio:
		template = loader.get_template('predictor/portfolio_detail.html')
		context = {
			'portfolio' : portfolio
		}
		return HttpResponse(template.render(context, request))
	else:
		return render(request, 'predictor/error.html', {
			'error_message': "Portfolio doesn't exist.",
		})


def error(request):
	return HttpResponse("An Error occured.")

def stock_detail(request, stock_ticker):
	if request.method == "POST":
		ticker = request.POST['ticker']
	else:
		ticker = stock_ticker
	API = stockAPI()
	stock = API.getStock(ticker)

	if not stock:
		return render(request, 'predictor/error.html', {
			'error_message': "Stock does not exist",
		})
	else:
		interface = stockDayDatabaseInterface()
		days = interface.getAllDaysOrdered(stock)
		array = []
		for day in days:
			array.append({'date' : day.day.strftime("%d-%b-%y"), 'close' : day.adjustedClose})
		days = json.dumps(array)
	template = loader.get_template('predictor/stock_detail.html')
	context = {
		'data' : days,
	}
	return HttpResponse(template.render(context, request))

def create_portfolio(request):
	template = loader.get_template('predictor/create_portfolio.html')
	context = {}
	return HttpResponse(template.render(context, request));

def make_portfolio(request):
	if request.method == "POST":
		current_user = request.user
		API = stockAPI()
		portfolio = Portfolio()
		portfolio.portfolio_name = request.POST['name']
		portfolio.investor = Investor.objects.get(user=current_user)
		portfolio.save()
		stocks = request.POST['stock-tickers'].split()
		stock_owned = Stock_Owned()
		stock = stocks[0]
		quantity = stocks[1]
		stock = API.getStock(stock)
		if not stock:
			return render(request, 'predictor/error.html', {
				'error_message': "Stock doesn't exist.",
			})
		stock_owned.portfolio = portfolio
		stock_owned.stock = stock
		stock_owned.bought_on = datetime.date.today()
		stock_owned.bought_at = stock.current_high
		stock_owned.amount_owned = quantity
		return HttpResponseRedirect(reverse('predictor:home', args=(current_user.id,)))
	else:
		return render(request, 'predictor/error.html', {
			'error_message': "You didn't submit a portfolio.",
		})


#JSON Response Areas for AJax Calls
def recommend_portfolio(request):
	if request.method == "POST":
		type = request.POST['type']
		totalspend = request.POST['total_spend']
		totalspend = float(totalspend)
		kwargs = {'budget':totalspend}
		if type == "control":
			return recommend_interfacer(recommend_type='random', budget=totalspend)
		elif type == "tsr":
			return recommend_interfacer(recommend_type='high_return', budget=totalspend)
		else:
			return recommend_interfacer(recommend_type='diverse', budget=totalspend)

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

