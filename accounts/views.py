# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaulttags import register

from .forms import CustomUserCreationForm, CustomUserChangeForm
    
    
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

        
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UpdateUserView(LoginRequiredMixin, generic.UpdateView):
    
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('landing-page')
    template_name = 'registration/updateUser.html'
    
    def get_object(self, queryset=None): 
        return self.request.user


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "settings.html"
