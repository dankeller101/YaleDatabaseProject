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
    #example /home
    url(r'^(?P<user_id>[0-9]+)/home', views.home, name='home')
]