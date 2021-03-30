'''
Created on Jan 17, 2014

@author: Muneeb
'''
from accounts.models import ShadowingProgramUser
from applicants.models import Applicant
# from core.models import Package
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def user_applicant_create(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also an applicant type user.
    Also if the user has created profile before it will redirect it to edit profile page.
    """
    def _user_applicant_create(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.role == ShadowingProgramUser.APPLICANT:
                try:
                    if user.applicant:
                        return HttpResponseRedirect(reverse('applicant-profile-edit', kwargs={'pk':user.applicant.pk}))
                except Applicant.DoesNotExist:
                    return view_func(request, *args, **kwargs)
            else:
                messages.add_message(request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(request, messages.ERROR, _("You must be logged in before performing this operation."))
            return HttpResponseRedirect(reverse('index'))

    return wraps(view_func)(_user_applicant_create)


def user_applicant_update(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also an it is also an applicant type user.
    Other wise set an error message.
    """
    def _user_applicant_update(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.role == ShadowingProgramUser.APPLICANT:
                try:
                    if user.applicant:
                        return view_func(request, *args, **kwargs)
                except Applicant.DoesNotExist:
                    return HttpResponseRedirect(reverse('applicant-profile-create'))
            else:
                messages.add_message(request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(request, messages.ERROR, _("You must be logged in before performing this operation."))
            return HttpResponseRedirect(reverse('index'))
    return wraps(view_func)(_user_applicant_update)


                
        
        

