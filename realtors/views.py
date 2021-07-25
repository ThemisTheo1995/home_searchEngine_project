from django.shortcuts import render, reverse
from django.views import generic
from django.http import JsonResponse
from django.core.mail import send_mail
from .mixins import RealtorAndLoginRequiredMixin, OrganisationAndLoginRequiredMixin
from .models import Organisation, Agent
from properties.models import Properties
from .forms import OrganisationUpdateForm, AgentModelAddForm


### Organisation dashboard ###
class OrganisationDashboardView(RealtorAndLoginRequiredMixin, generic.DetailView):
    template_name = "realtors/realtors_organisation_dashboard.html"
    context_object_name = 'organisation'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_realtor:
            queryset = Organisation.objects.filter(user = user)
        return queryset

### Organisation update ###
class OrganisationUpdateView(RealtorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "realtors/realtors_organisation_update.html"
    form_class = OrganisationUpdateForm
    context_object_name = 'organisation'
    
    def get_queryset(self): 
        return Organisation.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("organisation:organisation-dashboard", kwargs={'pk': self.request.user.organisation.pk})

### Organisation list ###
class OrganisationProperties(OrganisationAndLoginRequiredMixin, generic.ListView):
    template_name = "realtors/realtors_organisation_list_properties.html" 
    context_object_name = "organisation"
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        ###--- Logged in user is the Realtor/Organisation ---###
        if user.is_realtor:
            # We access directly the organisation id from user. User IS the Organisation.
            organisation = user.organisation
            q = Properties.objects.filter(organisation = organisation, advertised = 'To_Rent')
            properties = q.count()
            featured = q.filter(property_category='FEATURED').count()
            published = q.filter(is_published=True).count
        ###--- Logged in user is an Agent ---###
        elif user.is_agent:
            # We access the organisation id through the Agent model.
            organisation = user.agent.organisation
            q = Properties.objects.filter(organisation = organisation, advertised = 'To_Rent')
            # Agent has access only to associated properties
            # queryset = q.filter(agent__user = user)
            properties = q.count()
            featured = q.filter(property_category='FEATURED').count()
            published = q.filter(is_published=True).count
        
        context['properties'] = properties
        context['featured'] = featured
        context['published'] = published
        context['org'] = organisation
        context['charges'] = "15€"
        return context

    def get_queryset(self):
        user = self.request.user
        ###--- Logged in user is the Realtor/Organisation ---###
        if user.is_realtor:
            organisation = user.organisation
            queryset = Properties.objects.filter(
                organisation = organisation,
                advertised = 'To_Rent'
                ).order_by('-list_date')
        ###--- Logged in user is an Agent ---###
        elif user.is_agent:
            organisation = user.agent.organisation
            queryset = Properties.objects.filter(
                organisation = organisation,
                advertised = 'To_Rent'
                ).order_by('-list_date')
            # Agent has access only to associated properties
            # queryset = q.filter(agent__user = user)
        return queryset

def realtors_org_rent_preview(request):
    if  request.is_ajax and request.method == 'GET':
        try:
            rent = Properties.objects.get(pk=request.GET.get('pk', ''))
            data = {
                "rent": rent.bathrooms,
                "list_date": rent.list_date.strftime("%d/%m/%Y"),
                "address": rent.address,
                "photo_main": request.build_absolute_uri(rent.photo_main.url),
                "street_number": rent.street_number,
                "price": rent.price,
                "property_type": rent.property_type,
                "currency": rent.currency,
                "bedrooms": rent.bedrooms,
                "bathrooms": rent.bathrooms,
                "postalcode": rent.postalcode,
                "m2":rent.m2,
                "short_description":rent.short_description,
                "admin_1":rent.admin_1,
                "admin_2":rent.admin_2,
                "admin_3":rent.admin_3,
                "admin_4":rent.admin_4,
                "country":rent.country,
                "admin_1_en":rent.admin_1_en,
                "admin_2_en":rent.admin_2_en,
                "admin_3_en":rent.admin_3_en,
                "admin_4_en":rent.admin_4_en,
                "country_en":rent.country_en,
            }
        except:
            data = {
                "pk": "notFound"
            }
        return JsonResponse(data, status=200)
    
### Agents list ###
class AgentListView(RealtorAndLoginRequiredMixin, generic.ListView):
    paginate_by = 15
    template_name = "realtors/realtors_agent_list.html" 
    context_object_name = "agents"
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_realtor:
            if self.request.GET.get('agentid', ''):
                agentId = self.request.GET.get('agentid', '')
                agent = Agent.objects.get(pk = agentId)
                if  agent.active_agent:
                    Agent.objects.filter(id = agentId).update(active_agent = False)
                else:
                    Agent.objects.filter(id = agentId).update(active_agent = True)
                
            organisation = user.organisation
            q = Agent.objects.filter(organisation = organisation)
            agents = q.count()
        
        context['agentsNo'] = agents
        context['organisation'] = organisation
        
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_realtor:
            organisation = user.organisation
            queryset = Agent.objects.filter(organisation = organisation).order_by('-list_date')
            
        return queryset

### Agents update ###
class AgentCreateView(RealtorAndLoginRequiredMixin, generic.CreateView):
    template_name = "realtors/realtors_agent_create.html"
    form_class = AgentModelAddForm
    
    def get_success_url(self):
        return reverse("organisation:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_agent = True
        user.is_realtor = False
        user.set_password(user.username)
        user.save()
        Agent.objects.create(
            user = user,
            organisation = self.request.user.organisation 
        )
        send_mail(
            subject = "Genesis Estate - Agent invitation.",
            message = "You are added as an agent on Genesis Estate. Please login and reset your password.",
            from_email = "themistheodoratos@outlook.com",
            recipient_list = [user.email] 
        )
        return super(AgentCreateView, self).form_valid(form)


