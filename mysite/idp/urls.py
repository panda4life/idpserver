# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 10:44:57 2014

@author: James Ahad
"""

from django.conf.urls import patterns, url
from idp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^add_sequence/', views.addsequence, name='add_sequence'),
        url(r'^about/', views.about, name='about'),)