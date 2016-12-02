from django.conf.urls import url

from . import views, access_views, api_views

urlpatterns = [
    # example /
    url(r'^$', views.index, name='index'),
    
    # User access functions (login, register etc)
    url(r'^register', access_views.register, name='register'),
    url(r'^login', access_views.login, name='login'),
    url(r'^logout', access_views.logout, name='logout'),

    #example /error
    url(r'^error', views.error, name='error'),
    #example /1/home
    url(r'^home', views.home, name='home'),
    
    #example /stock/view/GOOGL
    url(r'^stock/view/(?P<stock_ticker>[a-z]+)', views.stock_detail, name='stock_detail'),
    #example /portfolio/create
    url(r'^portfolio/create', views.create_portfolio, name='create_portfolio'),
    #example /portfolio/make
    url(r'^portfolio/make', views.make_portfolio, name='make_portfolio'),
    #example /portfolio/view/1
    url(r'^portfolio/view/(?P<portfolio_id>[0-9]+)', views.portfolio_detail, name='portfolio_detail'),
    #example /portfolio/recommend
    # url(r'^api/get_recommendation', api_views.get_recommendation, name='get_recommendation'),
    # #example /portfolio/1
    # url(r'^portfolio/(?P<portfolio_id>[0-9]+)', views.portfolio_detail_json, name='portfolio_detail_json'),
    #example /portfolios
    # url(r'^portfolios', views.account_portfolios_json, name='account_portfolios_json'),

    # JSON API below
    url(r'^api/get_recommendation', api_views.get_recommendation, name='get_recommendation'),
    url(r'^api/portfolios/(?P<id>[0-9]+)', api_views.portfolio, name='api_portfolio'),
    url(r'^api/portfolios', api_views.portfolios, name='api_portfolios'),

    url(r'^api/get_stock_plot', api_views.get_stock_plot, name='get_stock_plot'),
]