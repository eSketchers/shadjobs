'''
Created on May 11, 2014

@author: Muneeb
'''
from django.conf.urls import patterns, url
from agencies.views import AgencyProfileUpdate
from applicants.views import ApplicantProfileCreate
from applicants.views import ApplicantsObservaApply

urlpatterns = patterns('',
    url(r'^profile/create/$', ApplicantProfileCreate.as_view(), name="applicant-profile-create"),
    url(r'^profile/(?P<pk>\d+)/edit/$', AgencyProfileUpdate.as_view(), name="applicant-profile-edit"),
    url(r'^apply/observa/$', ApplicantsObservaApply.as_view(), name="appicant-apply-observa"),
)