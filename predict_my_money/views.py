from django.shortcuts import render
from django.template import loader
from .models import User, Investor, Stock, Portfolio, Stock_Owned
from django.urls import reverse
from predict_my_money.utils import stockAPI
import datetime
from django.contrib.auth import authenticate, login, logout
from predict_my_money.computations.recommender_interface import recommend_diverse_portfolio, recommend_high_return_portfolio, recommend_random_portfolio

# Create your views here.


from django.http import HttpResponseRedirect, HttpResponse, Http404

def index(request):
	return HttpResponse("Hello, world.  You're at the polls index.")

def user_registration(request):
	template = loader.get_template('predictor/user_registration.html')
	context = {}
	return HttpResponse(template.render(context, request))

def portfolio_detail(request, portfolio_id):
	try:
		portfolio = Portfolio.objects.get(pk=portfolio_id)
	except Portfolio.DoesNotExist:
		return render(request, 'predictor/error', {
			'error_message': "Portfolio does not exist",
		})
	else:
		template = loader.get_template('predictor/portfolio_detail.html')
		context = {
			'portfolio' : portfolio
		}
		return HttpResponse(template.render(context, request))

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
		return render(request, 'predictor/error', {
			'error_message': "Stock does not exist",
		})
	template = loader.get_template('predictor/stock_detail.html')
	context = {
		'stock' : stock,
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
			return render(request, 'predictor/error', {
				'error_message': "Stock doesn't exist.",
			})
		stock_owned.portfolio = portfolio
		stock_owned.stock = stock
		stock_owned.bought_on = datetime.date.today()
		stock_owned.bought_at = stock.current_high
		stock_owned.amount_owned = quantity
		return HttpResponseRedirect(reverse('predictor:home', args=(current_user.id,)))
	else:
		return render(request, 'predictor/error', {
			'error_message': "You didn't submit a portfolio.",
		})

def sign_out(request):
	logout(request)
	return HttpResponse('You have successfully signed out.')



def create_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		name = request.POST['name']
		name = name.split()
		user = User.objects.create_user(username, email, password)
		user.first_name = name[0]
		user.last_name = name[1]
		user.save()
		investor = Investor()
		investor.user = user
		investor.save()
		login(request, user)
		return HttpResponseRedirect(reverse('predictor:home', args=(user.id,)))
	else:
		return render(request, 'predictor/error', {
			'error_message': "You didn't select a choice.",
		})

def log_in(request):
	template = loader.get_template('predictor/log_in.html')
	context = {}
	return HttpResponse(template.render(context, request));

def authenticate_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('predictor:home', args=(user.id,)))
		else:
			return render(request, 'predictor/error', {
				'error_message': "Invalid Login.",
			})

def home(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		raise Http404("User does not exist")
	else:
		investor = Investor.objects.get(user=user_id)
		return render(request, 'predictor/home.html', {'investor': investor, 'user': user})




#JSON Response Areas for AJax Calls
def recommend_portfolio(request):
	if request.method == "POST":
		type = request.POST['type']
		totalspend = request.POST['total_spend']
		return []
		# if type == "control":
		# 	return create_portfolio('random');
		# elif type == "tsr":
		# 	return create_portfolio('high_return');
		# else:
		# 	return create_portfolio('diverse');




