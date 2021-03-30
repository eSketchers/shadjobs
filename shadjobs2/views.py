'''
Created on May 9, 2014

@author: Muneeb
'''

from accounts.forms import LoginForm
from django.views.generic.edit import FormView


class Index(FormView):
    template_name='index.html'
    form_class = LoginForm