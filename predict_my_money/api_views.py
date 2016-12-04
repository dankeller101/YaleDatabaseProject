"""api_views.py"""

import datetime
import json

from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from predict_my_money.utils import stockAPI, portfolioAPI, \
	stockDayDatabaseInterface
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404, \
	HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods, require_GET

from .models import User, Investor, Stock, Portfolio, Stock_Owned, Portfolio_Day
from predict_my_money.computations.recommender_interface import \
	recommend_diverse_portfolio, recommend_high_return_portfolio, \
	recommend_random_portfolio, recommend_interfacer

sapi = stockAPI()
papi = portfolioAPI()

# Create your views here.
def portfolio_detail(request, portfolio_id):
	portfolio = papi.getPortfolio(portfolio_id)
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

#


@require_GET
def get_portfolio_plot(request):
	ticker = request.GET["stock"]
	stock = sapi.getStock(ticker)

	if not stock:
		return JsonResponse({ "data": None }, status=404)

	interface = stockDayDatabaseInterface()
	days = interface.getAllDaysOrdered(stock)
	array = []
	for day in days:
		array.append({'date' : day.day.strftime("%d-%b-%y"), 'close' : day.adjustedClose})

	return JsonResponse({ "data": array })


@require_GET
def get_stock(request):
	ticker = request.GET["name"]
	stock = sapi.getStock(ticker)

	if not stock:
		return JsonResponse({ "data": None }, status=404)

	return JsonResponse({
		"data": {
		    "stock_name": stock.stock_name, 
		    "company_name": stock.company_name, 
		    "company_meta": stock.company_meta, 
		    "current_high": stock.current_high, 
		    "current_low": stock.current_low, 
		    "current_adjusted_close": stock.current_adjusted_close, 
		    "start_date": stock.start_date, 
		    "end_date": stock.end_date, 
		}
	})

@require_GET
def get_stock_plot(request):
	ticker = request.GET["stock"]
	stock = sapi.getStock(ticker)

	if not stock:
		return JsonResponse({ "data": null }, status=404)

	interface = stockDayDatabaseInterface()
	days = interface.getAllDaysOrdered(stock)
	array = []
	for day in days:
		array.append({'date' : day.day.strftime("%d-%b-%y"), 'close' : day.adjustedClose})

	return JsonResponse({ "data": array })

@require_GET
def gen_portfolio_price_plot(request):
	stocks = json.loads(request.GET['stocks'])
	interface = stockDayDatabaseInterface()
	alldays = {}

	for key in stocks:
		stockinfo = stocks[key]
		stock = sapi.getStock(stockinfo["name"])
		if not stock:
			continue
		for stockday in interface.getAllDaysOrdered(stock):
			obj = {
				"name": stockinfo["name"],
				"price": stockday.adjustedClose,
				"date": stockday.day.strftime("%d-%b-%y")
			}

			key = stockday.day.strftime("%d-%b-%y")
			if not key in alldays:
				alldays[key] = []
			alldays[key].append(obj)

	result = []
	keylist = alldays.keys()
	keylist.sort()
	for key in keylist:
		result.append(alldays[key])
	    # print "%s: %s" % (key, alldays[key])

	return JsonResponse({ "data": result })

@require_GET
def get_recommendation(request):
	totalspend = float(request.GET['total_spend'])
	kwargs = { 'budget': totalspend }

	if "type" in request.GET and request.GET["type"] in ["random", "diverse"]:
		rtype = request.GET["type"]
	else:
		rtype = "high_return"

	a = recommend_interfacer(recommend_type=rtype, budget=totalspend)
	print(a)
	ret = []
	for m in a:
		print(m, a[m])
		ret.append([m, a[m][0], a[m][1]])
	print(ret)
	return JsonResponse({ "data": ret })

def portfolio(request, id):
	if request.method == "GET":
		portfolio = papi.getPortfolio(id)
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
	elif request.method == "POST":
		return HttpResponseBadRequest("Not implemented.")
	else:
		return HttpResponseBadRequest("Invalid method.")

def portfolios(request):
	if request.method == "GET":
		investor = Investor.objects.get(user=request.user)
		portfolios = Portfolio.objects.filter(investor=investor)
		storage = {}
		for portfolio in portfolios:
			storage[portfolio.portfolio_name] = [portfolio.current_value, portfolio.current_diversity]
		return HttpResponse(json.dumps(storage), content_type="application/json")
	
	elif request.method == "POST":
		portfolio = Portfolio()
		portfolio.portfolio_name = request.POST['name']
		portfolio.start_date = datetime.datetime.today()
		portfolio.end_date = datetime.datetime.today() - datetime.timedelta(days=10000000000)
		portfolio.investor = Investor.objects.get(user=request.user)
		portfolio.save()

		stocks = json.loads(request.POST["_stocks"])

		for order in stocks:
			sname = order['name']
			quantity = order['amount']

			stock = sapi.getStock(sname)
			if not stock:
				return JsonResponse({ "error": True, "message": "Stock not found." })

			owned = Stock_Owned()
			owned.portfolio = portfolio
			owned.stock = stock
			owned.bought_on = datetime.date.today()
			owned.bought_at = stock.current_high
			owned.amount_owned = quantity
			owned.save()

		return JsonResponse({ "error": False })
		# return HttpResponseRedirect(reverse('predictor:home', args=(current_user.id,)))
	else:
		return HttpResponseBadRequest("Invalid method.")