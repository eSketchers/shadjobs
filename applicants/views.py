# Create your views here.
from django.views.generic import ListView
from applicants.decorators import user_applicant_create
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from agencies.models import Agency, AgencyServices, Location
from applicants.models import Applicant
from applicants.forms import ApplicantFormCreate
from django.shortcuts import render_to_response
from django.template import RequestContext

class ApplicantProfileCreate(CreateView):
    template_name = "applicants/form_miperfil.html"
    model = Applicant
    form_class = ApplicantFormCreate
    
    @method_decorator(user_applicant_create)
    def dispatch(self, request, *args, **kwargs):
        return super(ApplicantProfileCreate, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **context):
        context = super(ApplicantProfileCreate, self).get_context_data(**context)
        all_services = AgencyServices.objects.all()
        context['all_services'] = all_services
        return context
    
    
    def form_valid(self, form):
        print 'form_valid'
        return super(ApplicantProfileCreate, self).form_valid(form)
    
    
    
# class AgencyProfileUpdate(UpdateView):
#     template_name = "agencies/agency_profile2.html"
#     model = Agency
#     form_class = AgencyFormUpdate
#     
#     
#     def dispatch(self, request, *args, **kwargs):
#         return super(AgencyProfileCreate, self).dispatch(request, *args, **kwargs)
#     
#     def get_success_url(self):
#         agency_id = self.kwargs['pk']
#         return reverse('agency-profile-edit', kwargs={'pk': agency_id})
#     
#     def get_initial(self):
#         if self.kwargs['pk']:
#             agency = get_object_or_404(Agency, pk=self.kwargs['pk'])
#             my_dict = {'state_province':agency.agency_location.state_province, 
#                     'agency_address':agency.agency_location.address,
#                     'agency_city':agency.agency_location.city,
#                     'agency_services': agency.agency_services.all()
#                     }
#             return my_dict
#     
#     def get_context_data(self, **context):
#         context['is_edit'] = True
#         return context

class ApplicantsObservaApply(ListView):
    template_name = 'applicants/form_observa.html'
    queryset = Agency.objects.all().order_by('agency_location__city')
    context_object_name = 'agencies'

    def get_context_data(self, **context):
        context = super(ApplicantsObservaApply, self).get_context_data(**context)
        context['agency_services'] = AgencyServices.objects.all()
        context['provinces'] = Location.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return render_to_response('applicants/filter_applicants_observa.html', {'agencies': self.get_queryset()},
                                      RequestContext(self.request))
        return super(ApplicantsObservaApply, self).render_to_response(context, **response_kwargs)

    def get_queryset(self):
        if self.request.is_ajax():
            if 'sort_by' in self.request.GET and 'provincia' in self.request.GET\
                and 'aptitudes' in self.request.GET and 'estado' in self.request.GET:

                sort_by = self.request.GET['sort_by'].lower()
                provincia = self.request.GET['provincia'].lower()
                aptitudes = self.request.GET['aptitudes'].lower()
                estado = self.request.GET['estado'].lower()

                final_result = Agency.objects.all()

                # date
                if sort_by == 'fech_down':
                    final_result = final_result.order_by('available_dates__available_date')

                # by agency name
                elif sort_by == 'vot_down':
                    final_result = final_result.order_by('agency_name')

                # by city
                else:
                    final_result = final_result.order_by('agency_location__city')

                if provincia != "":
                    final_result = final_result.filter(agency_location__state_provice__iexact=provincia)

                if aptitudes != 'todas':
                    final_result = final_result.filter(agency_services__service_name__iexact=aptitudes)

                if estado != 'todas':
                    final_result = final_result.filter(agency_services__service_name__iexact=estado)

                return final_result


        return Agency.objects.all().order_by('agency_location__city')
    
    
    
    