'''
Created on Jan 17, 2014

@author: Muneeb
'''
from accounts.models import ShadowingProgramUser
from agencies.models import Agency
# from core.models import Package
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def user_agency_create(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also an agency owner.
    Also if the user has created agency before it will redirect it to edit agency profile page.
    """
    def _user_agency_create(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            # The user is valid. Continue to the admin page.
            if user.role == ShadowingProgramUser.AGENCY:
                try:
                    if user.agency:
                        return HttpResponseRedirect(reverse('agency-profile-edit', kwargs={'pk':user.agency.pk}))
                except Agency.DoesNotExist:
                    return view_func(request, *args, **kwargs)
            else:
                messages.add_message(request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(request, messages.ERROR, _("You must be logged in before performing this operation."))
            return HttpResponseRedirect(reverse('index'))

    return wraps(view_func)(_user_agency_create)


def user_agency_update(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also an agency owner.
    Other wise set an error message.
    """
    def _user_agency_update(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.role == ShadowingProgramUser.AGENCY:
                try:
                    if user.agency:
                        return view_func(request, *args, **kwargs)
                except Agency.DoesNotExist:
                    return HttpResponseRedirect(reverse('agency-profile-create'))
            else:
                messages.add_message(request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(request, messages.ERROR, _("You must be logged in before performing this operation."))
            return HttpResponseRedirect(reverse('index'))
    return wraps(view_func)(_user_agency_update)

# def user_package_status_check(view_func):
#     def _user_package_status_check(request, *args,** kwargs):
#         user=request.user
#         if user.is_authenticated():
#             status=Package.objects.filter(user=user).order_by('-id')[:1]
#             if status:
#                 if status[0].is_activate==1:
#                     request.session['status']=1
#                     return view_func(request, *args, **kwargs)
#                 elif status[0].is_activate==2:
#                     request.session['status']=2
#                     return view_func(request, *args, **kwargs)
#                 else:
#                     request.session['status']=3
#                     return view_func(request, *args, **kwargs)
#             else:
#                 request.session['status']=4
#                 return view_func(request, *args, **kwargs)
#         else:
#             request.session['status']=4
#             return view_func(request, *args, **kwargs)
#     return wraps(view_func)(_user_package_status_check)

                
        
        

