# -*- coding: utf-8 -*- 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
# from django.utils import timezone as dj_datetime
# import time
from django.contrib.auth import get_user_model
from utils import STATES, file_upload_to, validate_number

#     return result
# Create your models here.
# 
# def file_upload_to(instance, filename):
#     return '/'.join([instance.__class__.__name__, unicode(dj_datetime.now().strftime('%Y/%m/%d')),
#             unicode( int(time.time()))+filename])


class Agency(models.Model):
    agency_owner = models.OneToOneField(get_user_model(), null=True, blank=True, verbose_name=_("Agency Owner"), related_name="agency")
    agency_name = models.CharField(verbose_name=_("Agency Name"), max_length=1000, null=False, blank=False)
    agency_url = models.URLField(verbose_name=_("Agency Url"), max_length=2048, null=True, blank=True)
    agency_logo = models.ImageField(verbose_name=_("Agency Logo"), upload_to=file_upload_to, 
                                    max_length=2000, null=True, blank=True)
    contact_person_name = models.CharField(verbose_name=_("Contact Person Name"), max_length=200, 
                                           null=False, blank=False)
    contact_person_surname = models.CharField(verbose_name=_("Contact Person Surname"), max_length=100, 
                                              null=False, blank=False)
    agency_email = models.EmailField(verbose_name=_("Agency Email"), null=False, blank=False)
    agency_linkedin_profile = models.URLField(verbose_name=_("Linkedin Profile"), max_length=2000, 
                                              null=True, blank=True)
    agency_telephone = models.CharField(verbose_name=_("Telephone"), validators=[validate_number], max_length=30, null=True, blank=True)
    comments = models.TextField(verbose_name=_("Comments"), null=False, blank=False)
    agency_services = models.ManyToManyField('AgencyServices', related_name="agencies", verbose_name=_("Services offered by agency"))
    agency_location = models.OneToOneField('Location', verbose_name=_("Agency Location"), null=False, blank=False)
    agency_updated = models.DateTimeField(auto_now=True)
    agency_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')
    
    def __unicode__(self):
        return "%s" % self.agency_name
    
    def get_absolute_url( self ):
        """Return entry's URL"""
        return ( reverse('agency-profile-edit', kwargs={'pk': self.pk}) )
        
    
class AvailableShadowingDates(models.Model):
    available_date_from = models.DateTimeField(verbose_name=_("Available From Date"), null=False, blank=False)
    available_date_till = models.DateTimeField(verbose_name=_("Available Till Date"), null=False, blank=False)
    agency = models.ForeignKey(Agency, verbose_name=_("Agency"), related_name="available_dates", null=True, blank=True)


class AgencyServices(models.Model):
    service_name = models.CharField(verbose_name=_("Service"), max_length=1000, null=False, blank=False)
    question_for_candidates = models.CharField(verbose_name=_("Question For Candidates"), max_length=8000,
                                               null=True, blank=False, help_text=_('Question you want to ask Candidate \
                                               who shows interest in developing that skill'))
    
    class Meta:
        verbose_name = _('Service Provided by Agency')
        verbose_name_plural = _('Services Provided by Agency')
    
    def __unicode__(self):
        return "%s" % self.service_name
    
    
class Location(models.Model):
    country = models.CharField(verbose_name=_("Country"), default="Spain", max_length=100, null=False, blank=False)
    state_province = models.CharField(verbose_name=_("State"), choices=STATES, max_length=100, null=False, blank=False)
    city = models.CharField(verbose_name=_("City"), null=False, max_length=200, blank=False)
    address = models.CharField(verbose_name=_("Address"), max_length=3000, null=False, blank=False)
    
    class Meta:
        verbose_name = _('Agency Location')
        verbose_name_plural = _('Agencies Location')
    
    def __unicode__(self):
        return "%s" % self.city
    
    