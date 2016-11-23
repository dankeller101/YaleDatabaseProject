from django.shortcuts import render
from django.template import loader
from .models import User, Investor
from django.urls import reverse

# Create your views here.


from django.http import HttpResponseRedirect, HttpResponse, Http404

def index(request):
	return HttpResponse("Hello, world.  You're at the polls index.")

def user_registration(request):
	template = loader.get_template('predictor/user_registration.html')
	context = {}
	return HttpResponse(template.render(context, request))

def error(request):
	return HttpResponse("An Error occured.")

def create_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		name = request.POST['name']
		name = name.split()
		user = User()
		user.email = email
		user.username = username
		user.password = password
		user.first_name = name.pop()
		user.last_name = name.pop()
		user.save()
		investor = Investor()
		investor.portfolios = None
		investor.user = user
		investor.save()
		return HttpResponseRedirect(reverse('predictor:home', args=(user.id,)))
	else:
		return render(request, 'predictor/error', {
			'error_message': "You didn't select a choice.",
		})

def home(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		raise Http404("User does not exist")
	else:
		investor = Investor.objects.get(user=user_id)
		return render(request, 'predictor/home.html', {'investor': investor, 'user': user})



