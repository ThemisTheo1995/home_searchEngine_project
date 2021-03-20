# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
class UpdateUserView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('login')
    template_name = 'registration/updateUser.html'
    
    # get current user object
    def get_object(self, queryset=None): 
        return self.request.user
