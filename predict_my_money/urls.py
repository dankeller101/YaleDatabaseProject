from django.conf.urls import url

from . import views

urlpatterns = [
    # example /
    url(r'^$', views.index, name='index'),
    #example /registeruser
    url(r'^registeruser', views.user_registration, name='user_registration'),
    #example /create_user
    url(r'^create_user', views.create_user, name='create_user'),
    #example /error
    url(r'^error', views.error, name='error'),
    #example /1/home
    url(r'^(?P<user_id>[0-9]+)/home', views.home, name='home'),
    #example /stock/view/GOOGL
    url(r'^stock/view/(?P<stock_ticker>[a-z]+)', views.stock_detail, name='stock_detail'),
    #example /portfolio/create
    url(r'^portfolio/create', views.create_portfolio, name='create_portfolio'),
    #example /portfolio/make
    url(r'^portfolio/make', views.make_portfolio, name='make_portfolio'),
    #example /log_in
    url(r'^log_in', views.log_in, name='log_in'),
    #example /authenticate_user
    url(r'^authenicate_user', views.authenticate_user, name='authenticate_user'),
    #example /log_out
    url(r'^log_out', views.sign_out, name='sign_out'),
    #example /portfolio/view/1
    url(r'^portfolio/view/(?P<portfolio_id>[0-9]+)', views.portfolio_detail, name='portfolio_detail'),
    #example /portfolio/recommend
    url(r'^portfolio/recommend', views.recommend_portfolio, name='recommend_portfolio'),
]