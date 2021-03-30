# encoding: utf-8
import httplib2
import os
import urllib2

from accounts.forms import LoginForm
from accounts.models import ShadowingProgramUser
from agencies.models import Agency

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, logout
from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, redirect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from oauth2client.client import flow_from_clientsecrets


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

def get_flow(host):
    if host == 'dev.gobalo.es:888' or host == 'localhost:8000' or host == '127.0.0.1:8000':
        CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets_gobalo.json')
    
    return flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/plus.profile.emails.read',
        redirect_uri='http://'+host+'/accounts/oauth2callback')


def index(request):
    FLOW = get_flow(request.get_host())
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)


def auth_return(request):
    FLOW = get_flow(request.get_host())

    credential = FLOW.step2_exchange(request.REQUEST)
    http = httplib2.Http()
    http = credential.authorize(http)
    response = credential.token_response
    email = response['id_token']['email']
    is_conecta = False
    is_conecta_observa = False
    # ONLINE EXAM http://openbadges.es/es/certificadoEmitido/kaseyo23@gmail.com/bcd1a55e9b3ff4c9383033dea67465af/mkt/cert-mkt
    # The applicant have access to "conecta"
    # PHYSICAL EXAM http://openbadges.es/es/certificadoEmitido/kaseyo23@gmail.com/bcd1a55e9b3ff4c9383033dea67465af/mkt/cert-mktp
    # The applicant have access to "conecta" and "observa"
    try:
        connection = urllib2.urlopen('http://openbadges.es/es/certificadoEmitido/'+email+'/bcd1a55e9b3ff4c9383033dea67465af/mkt/cert-mkt')
        connection.close()
        is_conecta = True
    except urllib2.HTTPError, e:
        print e.getcode()

    try:
        connection = urllib2.urlopen('http://openbadges.es/es/certificadoEmitido/'+email+'/bcd1a55e9b3ff4c9383033dea67465af/mkt/cert-mktp')
        connection.close()
        is_conecta_observa = True
    except urllib2.HTTPError, e:
        print e.getcode()

    if is_conecta != False or is_conecta_observa != False:
        user = get_user_model().objects.get_or_create(email=email)
        user[0].backend = 'django.contrib.auth.backends.ModelBackend'
        if user[1] == True:
            user[0].role = ShadowingProgramUser.APPLICANT
            import uuid
            user[0].password = uuid.uuid4()
            user[0].save()
        auth_login(request, user[0])
        return HttpResponseRedirect(reverse('applicant-profile-create'))
    else:
        message = _("Lo sentimos, debes haber completado algún programa de Formacionactivate.es".decode('utf-8'))
        messages.add_message(request, messages.ERROR, message)
        return HttpResponseRedirect(reverse('index'))

@sensitive_post_parameters()
@csrf_protect
# @never_cache
def login(request):
    redirect_field_name=REDIRECT_FIELD_NAME
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')

            if email and password:
                user = authenticate(username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    try:
                        if user.role == ShadowingProgramUser.AGENCY and user.agency:
                            if redirect_to and redirect_to == '':
                                return redirect(reverse('agency-profile-edit'))
                            else:
                                return HttpResponseRedirect(redirect_to)
                        else:
                            return redirect(reverse('agency-profile-create'))
                    except Agency.DoesNotExist:
                        return redirect(reverse('agency-profile-create'))
                else:
#                     raise forms.ValidationError(_("Sorry, login credentials are invalid. Please try again."))
                    message = _("Sorry, login credentials are invalid. Please enter valid credentials.")
                    messages.add_message(request, messages.ERROR, message)
                    return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))




