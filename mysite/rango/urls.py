# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 10:33:56 2014

@author: James Ahad
"""

from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))