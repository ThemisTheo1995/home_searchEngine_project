from django.shortcuts import render, reverse
from django.views import generic
from django.core.mail import send_mail
from .mixins import RealtorAndLoginRequiredMixin, OrganisationAndLoginRequiredMixin
from .models import Organisation, Agent
from properties.models import Properties
from .forms import OrganisationUpdateForm, AgentModelForm

### Organisation ###
class OrganisationDashboardView(OrganisationAndLoginRequiredMixin, generic.DetailView):
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
        return reverse("realtors:organisation-dashboard", kwargs={'pk': self.request.user.organisation.pk})


class OrganisationProperties(OrganisationAndLoginRequiredMixin, generic.ListView):
    paginate_by = 15
    template_name = "realtors/organisation_properties.html" 
    context_object_name = "organisation"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.organisation
        # Initialise query
        q = Properties.objects.filter(organisation = user, advertised = 'To_Rent')
        properties = q.count()
        featured = q.filter(property_category='FEATURED').count()
        published = q.filter(is_published=True).count
        context['properties'] = properties
        context['featured'] = featured
        context['published'] = published
        context['charges'] = "15€"
        return context

    def get_queryset(self):
        user = self.request.user.organisation
        queryset = Properties.objects.filter(
            organisation = user,
            advertised = 'To_Rent'
            ).order_by('-list_date')
        return queryset


### Agents ###

class AgentCreateView(RealtorAndLoginRequiredMixin, generic.CreateView):
    template_name = "realtors/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("organisation:organisation-properties", kwargs={'pk': self.request.user.organisation.pk})
    
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