from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def user_logged_in_before(function):
    """
    Decorator for views to check if its a users first login.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_previously_logged_in is False:
            return redirect('first_login')
        else:
            return function(request, *args, **kwargs)

    return wrap