#from django.shortcuts import render
import xml.etree.ElementTree as ET
from agencies.models import Location, Agency, AvailableShadowingDates,\
    AgencyServices
from applicants.models import Location as ApplicantLocation, Studies, Experience,\
    ApplicantWishlistSkills
from django.http.response import HttpResponse
from django.views.generic import CreateView, UpdateView
from agencies.forms import AgencyFormCreate, AgencyFormUpdate
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from agencies.decorators import user_agency_create, user_agency_update
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from applicants.models import Applicant, AppliedFor
from django.template.context import RequestContext
from django.db.models.aggregates import Count
# Create your views here.


def temp_fill_cities(request):
    try:
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        tree = ET.parse(BASE_DIR+'/abc.txt')
        root = tree.getroot()
        for select in root.iter('select'):
            i = 0
            state = ''
            for option in select.iter('option'):
                if i==0:
                    state = option.text
                    i = i+1
                else:
                    location = Location(state_province=state, city=option.text)
                    location.save()
    except Exception as ex:
        return HttpResponse(ex)
    return HttpResponse()


class AgencyProfileCreate(CreateView):
    template_name = "agencies/agency_profile2.html"
    form_class = AgencyFormCreate
    
    @method_decorator(user_agency_create)
    def dispatch(self, request, *args, **kwargs):
        return super(AgencyProfileCreate, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.agency_owner = self.request.user
        return super(AgencyProfileCreate, self).form_valid(form)



class AgencyProfileUpdate(UpdateView):
    template_name = "agencies/agency_profile2.html"
    model = Agency
    form_class = AgencyFormUpdate
    
    @method_decorator(user_agency_update)
    def dispatch(self, request, *args, **kwargs):
        return super(AgencyProfileUpdate, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        agency_id = self.kwargs['pk']
        return reverse('agency-profile-edit', kwargs={'pk': agency_id})
    
    def get_initial(self):
        if self.kwargs['pk']:
            agency = get_object_or_404(Agency, pk=self.kwargs['pk'])
#             available_shadowing_dates = get_object_or_404(AvailableShadowingDates, agency=agency)
            my_dict = {'state_province':agency.agency_location.state_province, 
                    'agency_address':agency.agency_location.address,
                    'agency_city':agency.agency_location.city,
                    'agency_services': agency.agency_services.all(),
#                     'available_date_from':available_shadowing_dates.available_date_from,
#                     'available_date_till':available_shadowing_dates.available_date_till,
                    }
            return my_dict
    
    def form_valid(self, form):
        form.instance.agency_owner = self.request.user
        return super(AgencyProfileUpdate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(AgencyProfileUpdate, self).get_context_data(**kwargs)
        context['is_edit'] = True
        return context
    

class AgencyViewObserver(ListView):
    template_name = 'agencies/agencia_observa.html'
    queryset = Applicant.objects.all().order_by('applicant_location__state_province')
    context_object_name = 'applicants'

    @method_decorator(user_agency_update)
    def dispatch(self, request, *args, **kwargs):
        return super(AgencyViewObserver, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **context):
        context = super(AgencyViewObserver, self).get_context_data(**context)
        context['agency_services'] = AgencyServices.objects.all()
#         context['estudios'] = Studies.objects.filter(applicant=self.request.user.agency)
#         context['experiencia'] = Experience.objects.filter(applicant=self.request.user.agency)
#         context['especialidades'] = ApplicantWishlistSkills.objects.filter(applicant=self.request.user.agency)
        context['provinces'] = ApplicantLocation.objects.values('state_province').\
                                annotate(count=Count('state_province')).order_by('-count')[:8]
                                                
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return render_to_response('agencies/filter_agencia_observa.html', {'applicants_applied': self.get_queryset()},
                                      RequestContext(self.request))
        return super(AgencyViewObserver, self).render_to_response(context, **response_kwargs)

    def get_queryset(self):
        if self.request.is_ajax():
            if 'sort_by' in self.request.GET and 'provincia' in self.request.GET\
                and 'aptitudes' in self.request.GET and 'estado' in self.request.GET:

                sort_by = self.request.GET['sort_by'].lower()
                provincia = self.request.GET['provincia'].lower()
                aptitudes = self.request.GET['aptitudes'].lower()
                estado = self.request.GET['estado'].lower()

                final_result = AppliedFor.objects.filter(applied_at=self.request.user.agency)

                # date
                if sort_by == 'fech_down':
                    final_result = final_result.order_by('applied_for_date')
                    
                # date
                if sort_by == 'vot_down':
                    final_result = final_result.order_by('is_favourite')

                if provincia != "":
                    final_result = final_result.filter(applied_by__applicant_location__state_province__iexact=provincia)

                if aptitudes != 'todas':
                    final_result = final_result.filter(applied_at__agency_services__service_name__iexact=aptitudes)

                if estado != 'todas':
                    if estado == 'solicitado':
                        final_result = final_result.filter(current_status=AppliedFor.APPLY)
                    elif estado == 'admitido':
                        final_result = final_result.filter(current_status=AppliedFor.ACKNOWLEDGE)
                    elif estado == 'favoritos':
                        final_result = final_result.filter(is_favourite=True)
                return final_result

        return AppliedFor.objects.filter(applied_at=self.request.user.agency)\
                                        .order_by('applicant_location__state_province')
    
    
    
    