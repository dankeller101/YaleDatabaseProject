from django.conf.urls import url

from . import views, access_views

urlpatterns = [
    # example /
    url(r'^$', views.index, name='index'),
    #example /registeruser
    url(r'^register', access_views.register, name='register'),
    # #example /create_user
    # url(r'^create_user', access_views.create_user, name='create_user'),
    #example /log_in
    url(r'^log_in', access_views.login, name='login'),
    #example /authenticate_user
    # url(r'^authenticate_user', access_views.authenticate_user, name='authenticate_user'),
    #example /log_out
    url(r'^log_out', access_views.sign_out, name='logout'),

    #example /login/json
    url(r'^login/json', access_views.log_in_json, name="log_in_json"),
    #example /logout/json
    url(r'^logout/json', access_views.log_out_json, name="log_out_json"),

    #example /error
    url(r'^error', views.error, name='error'),
    #example /1/home
    url(r'^home', views.home0, name='home0'),
    #example /1/home
    url(r'^(?P<user_id>[0-9]+)/home', views.home, name='home'),
    #example /stock/view/GOOGL
    url(r'^stock/view/(?P<stock_ticker>[a-z]+)', views.stock_detail, name='stock_detail'),
    #example /portfolio/create
    url(r'^portfolio/create', views.create_portfolio, name='create_portfolio'),
    #example /portfolio/make
    url(r'^portfolio/make', views.make_portfolio, name='make_portfolio'),
    #example /portfolio/view/1
    url(r'^portfolio/view/(?P<portfolio_id>[0-9]+)', views.portfolio_detail, name='portfolio_detail'),
    #example /portfolio/recommend
    url(r'^portfolio/recommend', views.recommend_portfolio, name='recommend_portfolio'),
    #example /portfolio/1
    url(r'^portfolio/(?P<portfolio_id>[0-9]+)', views.portfolio_detail_json, name='portfolio_detail_json'),
    #example /portfolios
    url(r'^portfolios', views.account_portfolios_json, name='account_portfolios_json'),
]