from django.conf.urls import patterns, include, url

from django.contrib import admin
from shadjobs2.views import Index
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shadjobs2.views.home', name='home'),
    # url(r'^shadjobs2/', include('shadjobs2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^temp/$', temp_fill_cities),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^agency/', include('agencies.urls')),
    url(r'^applicants/', include('applicants.urls')),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


