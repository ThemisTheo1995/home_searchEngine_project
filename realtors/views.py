from django.shortcuts import render, reverse
from django.views import generic
from .mixins import RealtorAndLoginRequiredMixin
from .models import Realtor
from properties.models import Properties
from .forms import RealtorUpdateForm


class RealtorDashboardView(RealtorAndLoginRequiredMixin, generic.DetailView):
    template_name = "realtors/realtors_dashboard.html"
    context_object_name = 'realtor'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_realtor:
            queryset = Realtor.objects.filter(user = user)
            return queryset


class RealtorUpdateView(RealtorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "realtors/realtors_update.html"
    form_class = RealtorUpdateForm
    context_object_name = 'realtor'
    
    def get_queryset(self): 
        return Realtor.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("realtors:realtor-dashboard", kwargs={'pk': self.request.user.realtor.pk})


class RealtorProperties(RealtorAndLoginRequiredMixin, generic.ListView):
    paginate_by = 15
    template_name = "realtors/realtors_properties.html" 
    context_object_name = "realtor_rent"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.realtor
        # Initialise query
        q = Properties.objects.filter(realtor = user, advertised = 'To_Rent')
        properties = q.count()
        featured = q.filter(property_category='FEATURED').count()
        published = q.filter(is_published=True).count
        context['properties'] = properties
        context['featured'] = featured
        context['published'] = published
        context['charges'] = "15€"
        return context

    def get_queryset(self):
        user = self.request.user.realtor
        queryset = Properties.objects.filter(
            realtor = user,
            advertised = 'To_Rent'
            ).order_by('-list_date')
        return queryset
