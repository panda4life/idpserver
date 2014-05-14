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
        url(r'^about/', views.about, name='about'),
        url(r'^wl/', views.launch_wljob, name='wl'),
        url(r'^hetero/', views.launch_heterojob, name='hetero'),
        url(r'^profile/', views.profile, name='profile'),
        url(r'^joblist/', views.joblist, name='joblist'),
        url(r'^seqprop/', views.seqprop, name='seqprop'),
        url(r'^singleseqprop/', views.singleseqprop, name='singleseqprop'),)
