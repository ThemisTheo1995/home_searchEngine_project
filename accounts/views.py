# accounts/views.py
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from realtors.models import Organisation
from .forms import CustomUserCreationForm, CustomUserChangeForm
          
  
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save(commit = False)
        if user.is_realtor:
            user.save()
            Organisation.objects.create(
                user = user
                )
        return super(SignUpView, self).form_valid(form)

class UpdateUserView(LoginRequiredMixin, generic.UpdateView):
    
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('landing-page')
    template_name = 'registration/updateUser.html'
    
    def get_object(self, queryset=None): 
        return self.request.user

class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/settings.html"
