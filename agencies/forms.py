'''
Created on May 1, 2014

@author: Muneeb
'''
from django.forms import ModelForm
from agencies.models import Agency, Location,AvailableShadowingDates
from utils import STATES
from django import forms

class AgencyFormCreate(ModelForm):
    class Meta:
        model = Agency
        exclude = ['agency_updated', 'agency_created', 'agency_location', 'agency_owner']
    
    state_province = forms.ChoiceField(choices=STATES, required=True)
    agency_city = forms.CharField(required=True, max_length=200)
    agency_address = forms.CharField(required=True, max_length=3000)
    terms_condition = forms.BooleanField(required=True)
#     available_date_from = forms.DateTimeField(required=True)
#     available_date_till = forms.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        super(AgencyFormCreate, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        state_province_data = self.cleaned_data['state_province']
        agency_city_data = self.cleaned_data['agency_city']
        agency_address_data = self.cleaned_data['agency_address']
        agency_services = self.cleaned_data['agency_services']
        terms_condition_data = self.cleaned_data['terms_condition']
#         available_date_from_data = self.cleaned_data['available_date_from']
#         available_date_till_data = self.cleaned_data['available_date_till']
        agency = None
        if commit and terms_condition_data == 1:
            agency = super(AgencyFormCreate, self).save(commit=False)
            location = Location(state_province=state_province_data, city=agency_city_data, address=agency_address_data)
            location.save()
            agency.agency_location = location
            agency.save()
            for serv in agency_services:
                agency.agency_services.add(serv)
#         if available_date_from_data and available_date_till_data:
#             available_shodowing_dates = AvailableShadowingDates(available_date_from = available_date_from_data,
#                                                                 available_date_till = available_date_till_data, 
#                                                                 agency=agency)
#             available_shodowing_dates.save()
        return agency
    
    
class AgencyFormUpdate(ModelForm):
    class Meta:
        model = Agency
        exclude = ['agency_updated', 'agency_created', 'agency_location', 'agency_owner']
    
    state_province = forms.ChoiceField(choices=STATES, required=True)
    agency_city = forms.CharField(required=True, max_length=200)
    agency_address = forms.CharField(required=True, max_length=3000)
#     available_date_from = forms.DateTimeField(required=True)
#     available_date_till = forms.DateTimeField(required=True)
    
    
    def get_form_kwargs(self):
        kwargs = super(AgencyFormUpdate, self).get_form_kwargs()
#         kwargs.update({'place_user': self.request.user})
        return kwargs
    
    def save(self, commit=True):
        state_province_data = self.cleaned_data['state_province']
        agency_city_data = self.cleaned_data['agency_city']
        agency_address_data = self.cleaned_data['agency_address']
        agency_services = self.cleaned_data['agency_services']
#         available_date_from_data = self.cleaned_data['available_date_from']
#         available_date_till_data = self.cleaned_data['available_date_till']
        
        agency = self.instance
        if commit:
#             agency = super(AgencyFormUpdate, self).save()
            agency.agency_location.state_province = state_province_data
            agency.agency_location.city = agency_city_data
            agency.agency_location.address = agency_address_data
            agency.agency_location.save()
            agency.agency_services.clear()
            for serv in agency_services:
                agency.agency_services.add(serv)
            agency.save()
#         if available_date_from_data and available_date_till_data:
#             AvailableShadowingDates.objects.filter(agency=agency).update(available_date_from = available_date_from_data,
#                                                                          available_date_till = available_date_till_data)
        return agency
    
    
    
    