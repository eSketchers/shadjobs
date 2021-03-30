from django.contrib import admin
from agencies.models import Agency, AgencyServices, AvailableShadowingDates,\
    Location

# Register your models here.

admin.site.register(Agency)
admin.site.register(AgencyServices)
admin.site.register(AvailableShadowingDates)
admin.site.register(Location)