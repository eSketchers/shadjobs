'''
Created on May 1, 2014

@author: Muneeb
'''
from django.conf.urls import patterns, url
from agencies.views import AgencyProfileCreate, AgencyProfileUpdate,\
    AgencyViewObserver


urlpatterns = patterns('',
    url(r'^profile/create/$', AgencyProfileCreate.as_view(), name="agency-profile-create"),
    url(r'^profile/(?P<pk>\d+)/edit/$', AgencyProfileUpdate.as_view(), name="agency-profile-edit"),
    url(r'list/applicants/applied/$', AgencyViewObserver.as_view(), name="applicant-list-applied"),
)