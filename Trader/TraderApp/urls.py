from django.conf.urls import url
from TraderApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [

	url(r'^profiles/home/$', views.profile),	
	url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

]