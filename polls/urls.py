'''
Created on 4 Oct 2015

@author: khairulimam
'''

from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.index),
               url(r'^(?P<question_id>[0-9]+)/$', views.detail),
               url(r'^(?P<question_id>[0-9]+/result/$)', views.results, name="result"),
               url(r'^(?P<question_id>[0-9]+/vote/$)', views.vote, name="vote"),]