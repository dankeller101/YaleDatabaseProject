from django.conf.urls import url

from . import views

urlpatterns = [
    # example /
    url(r'^$', views.index, name='index'),
    #example /registeruser
    url(r'^register', views.register, name='register'),
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
    url(r'^authenticate_user', views.authenticate_user, name='authenticate_user'),
    #example /log_out
    url(r'^log_out', views.sign_out, name='sign_out'),
    #example /portfolio/view/1
    url(r'^portfolio/view/(?P<portfolio_id>[0-9]+)', views.portfolio_detail, name='portfolio_detail'),
    #example /portfolio/recommend
    url(r'^portfolio/recommend', views.recommend_portfolio, name='recommend_portfolio'),
    #example /portfolio/1
    url(r'^portfolio/(?P<portfolio_id>[0-9]+)', views.portfolio_detail_json, name='portfolio_detail_json'),
    #example /portfolios
    url(r'^portfolios', views.account_portfolios_json, name='account_portfolios_json'),
    #example /login/json
    url(r'^login/json', views.log_in_json, name="log_in_json"),
    #example /logout/json
    url(r'^logout/json', views.log_out_json, name="log_out_json"),
]