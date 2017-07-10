from django.conf.urls import url
from . import views

app_name = 'display'

urlpatterns = [
    #/display/
    url(r'^$', views.view_scoreboard, name='index'),
    #/display/morning/
    url(r'^morning/', views.morning, name='morning'),
    #display/forwarder<id>/
    url(r'^forwarder(\d+)/', views.view_forwarders, name = 'forwarders'),
    #url(r'^forwarder/', views.view_forwarders, name = 'forwarders'),
    #/display/time_query/
    url(r'^time_query/', views.get_table_time_query, name='table_time_query'),

]

