from django.shortcuts import render, reverse
from django.views import generic
from .mixins import RealtorAndLoginRequiredMixin
from .models import Realtor
from .forms import RealtorUpdateForm

# Create your views here.

class RealtorUpdateView(RealtorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "realtors/realtors_update.html"
    form_class = RealtorUpdateForm
    context_object_name = 'realtor'
    
    def get_queryset(self): 
        return Realtor.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("realtors:realtor-dashboard", kwargs={'pk': self.request.user.realtor.pk})


class RealtorDetailView(RealtorAndLoginRequiredMixin, generic.DetailView):
    template_name = "realtors/realtors_dashboard.html"
    context_object_name = 'realtor'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_realtor:
            queryset = Realtor.objects.filter(user = user)
            return queryset