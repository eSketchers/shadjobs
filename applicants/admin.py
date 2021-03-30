'''
Created on May 18, 2014

@author: Muneeb
'''
from django.contrib import admin
from applicants.models import Applicant, Location, Studies, Experience,\
    ApplicantCitiesOfInterest, ApplicantWishlistSkills, AppliedFor


admin.site.register(Applicant)
admin.site.register(Location)
admin.site.register(Studies)
admin.site.register(Experience)
admin.site.register(ApplicantCitiesOfInterest)
admin.site.register(ApplicantWishlistSkills)
admin.site.register(AppliedFor)
