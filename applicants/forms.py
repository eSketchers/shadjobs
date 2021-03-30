'''
Created on May 11, 2014

@author: Muneeb
'''
from django.forms.models import ModelForm
from applicants.models import Applicant, ApplicantCitiesOfInterest
from django import forms
from utils import STATES
from agencies.models import Location
from applicants.models import Location as ApplicantLocation
from django.db.models import Count

class ApplicantFormCreate(ModelForm):
    class Meta:
        model = Applicant
        exclude = ['applicant_updated', 'applicant_created', 'applicant_location', 'applicant_user']
    
    state_province = forms.ChoiceField(choices=STATES, required=True)
    cities_interest = forms.MultipleChoiceField(required=True, choices=STATES)
    terms_condition = forms.BooleanField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(ApplicantFormCreate, self).__init__(*args, **kwargs)
        cities_interest_choices = Location.objects.values('city').annotate(
                                                count=Count('city')).order_by('-count')[:8]
        cities_interest = ()
        for city in cities_interest_choices:
            cities_interest = cities_interest + ((city['city'],city['city']),)
        self.fields['cities_interest'].choices = cities_interest
    
    def save(self, commit=True):
        state_province_data = self.cleaned_data['state_province']
        cities_interest_data = self.cleaned_data['cities_interest']
        terms_condition_data = self.cleaned_data['terms_condition']
        applicant = None
        if commit and terms_condition_data == 1:
            applicant = super(ApplicantFormCreate, self).save(commit=False)
            location = ApplicantLocation(state_province=state_province_data)
            location.save()
            applicant.applicant_location = location
            applicant.save()
            for city in cities_interest_data:
                applicant_city_of_interest = ApplicantCitiesOfInterest(city=city, applicant=applicant)
                applicant_city_of_interest.save()
        return applicant
    
    
# class AgencyFormUpdate(ModelForm):
#     class Meta:
#         model = Agency
#         exclude = ['agency_updated', 'agency_created', 'agency_location']
#     
#     state_province = forms.ChoiceField(choices=STATES, required=True)
#     agency_city = forms.CharField(required=True, max_length=200)
#     agency_address = forms.CharField(required=True, max_length=3000)
#     
#     def save(self, commit=True):
#         state_province_data = self.cleaned_data['state_province']
#         agency_city_data = self.cleaned_data['agency_city']
#         agency_address_data = self.cleaned_data['agency_address']
#         agency_services = self.cleaned_data['agency_services']
#         agency = self.instance
#         if commit:
# #             agency = super(AgencyFormUpdate, self).save()
#             agency.agency_location.state_province = state_province_data
#             agency.agency_location.city = agency_city_data
#             agency.agency_location.address = agency_address_data
#             agency.agency_location.save()
#             agency.agency_services.clear()
#             for serv in agency_services:
#                 agency.agency_services.add(serv)
#             agency.save()
#         return agency