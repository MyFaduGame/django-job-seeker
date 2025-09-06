from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.is_authenticated and getattr(request.user, 'role', None) == role:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to view that page.")
            return redirect('accounts:login')
        return _wrapped
    return decorator

employer_required = role_required('employer')
jobseeker_required = role_required('jobseeker')
