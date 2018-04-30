from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^view_profile/(?P<id>\d+)$', views.view_profile),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'remove_friend/(?P<f_id>\d+)$', views.remove_friend)    
    ]
