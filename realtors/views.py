from django.shortcuts import render, reverse
from django.views import generic
from django.core.mail import send_mail
from .mixins import RealtorAndLoginRequiredMixin, OrganisationAndLoginRequiredMixin
from .models import Organisation, Agent
from properties.models import Properties
from .forms import OrganisationUpdateForm, AgentModelAddForm



### Organisation views ###

class OrganisationDashboardView(RealtorAndLoginRequiredMixin, generic.DetailView):
    template_name = "realtors/organisation_dashboard.html"
    context_object_name = 'organisation'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_realtor:
            queryset = Organisation.objects.filter(user = user)
        return queryset


class OrganisationUpdateView(RealtorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "realtors/organisation_update.html"
    form_class = OrganisationUpdateForm
    context_object_name = 'organisation'
    
    def get_queryset(self): 
        return Organisation.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("organisation:organisation-dashboard", kwargs={'pk': self.request.user.organisation.pk})


class OrganisationProperties(OrganisationAndLoginRequiredMixin, generic.ListView):
    paginate_by = 15
    template_name = "realtors/organisation_properties.html" 
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



### Agent views ###

class AgentListView(RealtorAndLoginRequiredMixin, generic.ListView):
    paginate_by = 15
    template_name = "realtors/agent_list.html" 
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
        
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_realtor:
            organisation = user.organisation
            queryset = Agent.objects.filter(organisation = organisation).order_by('-list_date')
            
        return queryset


class AgentCreateView(RealtorAndLoginRequiredMixin, generic.CreateView):
    template_name = "realtors/agent_create.html"
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
            from_email = "admin@test.com",
            recipient_list = [user.email] 
        )
        return super(AgentCreateView, self).form_valid(form)


