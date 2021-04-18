from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class RealtorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is realtor."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_realtor:
            return redirect("langind-page")
        return super().dispatch(request, *args, **kwargs)