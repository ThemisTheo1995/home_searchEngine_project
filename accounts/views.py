# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaulttags import register
from .messages import signUp, updateUser, settings

from .forms import CustomUserCreationForm, CustomUserChangeForm

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"
        
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = signUp
        return context
    
class UpdateUserView(LoginRequiredMixin, generic.UpdateView):
    
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('landing-page')
    template_name = 'registration/updateUser.html'
    
    def get_object(self, queryset=None): 
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = updateUser
        return context

class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "settings.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = settings
        return context