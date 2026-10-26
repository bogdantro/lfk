from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.urls import reverse


def staff_required(view_func):
    """Like Django's staff_member_required, but sends people to the site's own
    login page instead of the Django admin login."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect_to_login(request.get_full_path(), reverse('login'))
        return view_func(request, *args, **kwargs)
    return wrapper
