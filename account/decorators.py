from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # pour être sûr que l'utilisateur soit connecté
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_role(role_name):
                return HttpResponseForbidden("Accès refusé : rôle requis.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
