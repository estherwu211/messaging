from django.conf.urls import url
from . import views

app_name = 'display'

urlpatterns = [
    #/music/
    url(r'^$', views.view_scoreboard, name='index'),
    #/music/morning/
    url(r'^morning/', views.morning, name='morning'),
    #music/forwarder<id>/
    url(r'^forwarder(\d+)/', views.view_forwarders, name = 'forwarders'),
    #url(r'^forwarder/', views.view_forwarders, name = 'forwarders'),
]