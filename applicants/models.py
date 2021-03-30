from django.db import models
from django.contrib.auth import get_user_model
from utils import file_upload_to, validate_number, STATES
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from agencies.models import AgencyServices, Agency


# Create your models here.

class Applicant(models.Model):
    applicant_user = models.OneToOneField(get_user_model(), null=True, blank=True, 
                                        verbose_name=_("Applicant User"), related_name="applicant")
    applicant_name = models.CharField(verbose_name=_("Applicant Name"), max_length=1000, null=False, blank=False)
    applicant_cv = models.FileField(verbose_name=_("Applicant C.V."), upload_to=file_upload_to, 
                                    max_length=2000, null=True, blank=True)
    applicant_surname = models.CharField(verbose_name=_("Applicant Surname"), max_length=100, 
                                              null=False, blank=False)
#     agency_email = models.EmailField(verbose_name=_("Agency Email"), null=False, blank=False)
    applicant_linkedin_profile = models.URLField(verbose_name=_("Applicant Linkedin Profile"), max_length=2000, 
                                              null=True, blank=True)
    applicant_telephone = models.CharField(verbose_name=_("Telephone"), validators=[validate_number], 
                                        max_length=30, null=True, blank=True)
    comments = models.TextField(verbose_name=_("Comments"), null=False, blank=False)
#     agency_services = models.ManyToManyField('AgencyServices', related_name="agencies", 
#                                              verbose_name=_("Services offered by agency"))
    applicant_location = models.OneToOneField('Location', verbose_name=_("Applicant Location"), 
                                           null=False, blank=False)
    applicant_updated = models.DateTimeField(auto_now=True)
    applicant_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Applicant')
        verbose_name_plural = _('Applicants')
    
    def __unicode__(self):
        return "%s" % self.applicant_name
    
    def get_absolute_url( self ):
        """Return entry's URL"""
        return ( reverse('applicant-profile-edit', kwargs={'pk': self.pk}) )
    

class Location(models.Model):
    country = models.CharField(verbose_name=_("Country"), default="Spain", max_length=100, null=False, blank=False)
    state_province = models.CharField(verbose_name=_("State"), choices=STATES, max_length=100, null=False, blank=False)
    
    class Meta:
        verbose_name = _('Applicant\'s Location')
        verbose_name_plural = _('Applicant\'s Locations')
    
    def __unicode__(self):
        return "%s" % self.state_province
    

class Studies(models.Model):
    course_diploma_name = models.CharField(verbose_name=_("Course Name"), max_length=200, null=False, blank=False)
    applicant = models.ForeignKey(Applicant, verbose_name=_("Applicant"), related_name="studies", null=False, blank=False)
    
    class Meta:
        verbose_name = _('Studies')
        verbose_name_plural = _('Studies')
    
    def __unicode__(self):
        return "%s" % self.course_diploma_name
    

class Experience(models.Model):
    experience = models.CharField(verbose_name=_("Experience"), max_length=200, null=False, blank=False)
    applicant = models.ForeignKey(Applicant, verbose_name=_("Applicant"), related_name="experience", 
                                  null=False, blank=False)
    
    class Meta:
        verbose_name = _('Experience')
        verbose_name_plural = _('Experiences')
    
    def __unicode__(self):
        return "%s" % self.experience


class ApplicantCitiesOfInterest(models.Model):
    city = models.CharField(verbose_name=_("Applicant City Of Interest"), max_length=300, null=False, blank=False)
    applicant = models.ForeignKey(Applicant, verbose_name=_("Applicant"), related_name="applicant_cities_interest", 
                                  null=False, blank=False)

    class Meta:
        verbose_name = _('Applicant City Of Interest')
        verbose_name_plural = _('Applicant Cities Of Interest')

    def __unicode__(self):
        return "%s" % self.city


class ApplicantWishlistSkills(models.Model):
    applicant_skills = models.ForeignKey(AgencyServices, null=False, blank=False, verbose_name=_("Skill you wish to develop"), 
                                        related_name="applicant_skills_wishlist")
    applicant_question_comments = models.TextField(verbose_name=_("Comments"), null=False, blank=False)
    applicant = models.ForeignKey(Applicant, null=False, blank=False, verbose_name=_("Applicant"))

    class Meta:
        verbose_name = _('Skill, applicant like to develop')
        verbose_name_plural = _('Skills, applicants like to develop')

    def __unicode__(self):
        return "%s" % self.applicant_skills


class AppliedFor(models.Model):
    applied_by = models.ForeignKey(Applicant, verbose_name=_("Applicant"), related_name="applied_for",
                                   null=False, blank=False)
    applied_at = models.ForeignKey(Agency, verbose_name=_("Agency"), related_name="applicants",
                                   null=False, blank=False)

    applied_for_date = models.DateTimeField(verbose_name=_("Applied For Date"), null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    OBSERVER = 0
    JOB = 1
    APPLIED_FOR = ((OBSERVER, _('Observer')),
                (JOB, _('Job')),
            )

    applicant_applied_for = models.IntegerField(verbose_name=_("Applied For"), choices=APPLIED_FOR)
    
    APPLY = 0
    ACKNOWLEDGE = 1
    REJECT = 2
    STATUS = ((APPLY, _('Apply')),
                (ACKNOWLEDGE, _('Acknowledge')),
                (REJECT, _('Reject')),
            )

    current_status = models.IntegerField(verbose_name=_("Status"), choices=STATUS, default=APPLY)
    is_favourite = models.BooleanField(verbose_name=_("Is Favourite"), default=False)



