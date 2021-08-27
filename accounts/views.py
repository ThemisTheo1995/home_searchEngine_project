# accounts/views.py
from django.views import generic
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from realtors.models import Organisation
from properties.models import Properties, UserPropertyFavourite
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import redirect
          
  
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

class UserDashboardView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/accounts_myAccount.html"
    paginate_by = 15
    context_object_name = "properties"
    
    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        favourite = request.POST.get('property_id', None)
        notes = request.POST.get('note', None)
        e = UserPropertyFavourite.objects.get(user = user, favourite = favourite).pk
        UserPropertyFavourite.objects.filter(pk = e).update(notes=notes)
        return redirect("accounts:myaccount")
    
    def get_queryset(self):
        user = self.request.user.pk
        queryset = UserPropertyFavourite.objects.filter(user = user)
        return queryset
        
class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/accounts_settings.html"
