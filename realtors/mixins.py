from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class RealtorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is realtor."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_realtor:
            return redirect("landing-page")
        return super().dispatch(request, *args, **kwargs)

class OrganisationAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is agent or realtor."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_realtor:
            if not request.user.is_authenticated or not request.user.is_realtor:
                return redirect("landing-page")
        else:
            if not request.user.is_authenticated or not request.user.is_agent or not request.user.agent.active_agent:
                return redirect("landing-page")
        return super().dispatch(request, *args, **kwargs)