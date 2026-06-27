from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from .models import StartupIdea

class OwnerRequiredMixin(AccessMixin):
    """
    Verify that the current user is authenticated and is the owner of the requested StartupIdea.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        slug = kwargs.get('slug')
        idea = get_object_or_404(StartupIdea, slug=slug)
        
        if idea.owner != request.user:
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)
