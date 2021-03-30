'''
Created on May 6, 2014

@author: Muneeb
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^google/$', 'accounts.views.index'),
    url(r'^oauth2callback', 'accounts.views.auth_return'),
    
    url(r'auth-login/$', 'accounts.views.login', name='login-view'),
    url(r'logout/$', 'accounts.views.logout_view', name='logout-view'),
    
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'}, name="password_reset"),
    (r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
)

