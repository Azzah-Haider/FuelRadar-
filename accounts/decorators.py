from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def role_required(*roles):
    """
    Restricts a view to users whose `role` field matches one of the given roles.
    Usage: @role_required('manager') or @role_required('manager', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator