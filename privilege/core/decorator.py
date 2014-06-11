# -*- coding: utf-8 -*-
"""
Built-in permission_required leads to INF 302 redirect.
"""

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


__all__ = ['privilege_required', 'check_privilege', 'required_superuser']
admin_login = reverse_lazy("admin:index")


def required_superuser(view_func):
    @login_required(login_url=admin_login)
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrap


# decorator receive params, outer layer receives params for decorator itself
def privilege_required(perm_code):
    # middle layer receive target function
    def decorator(view_func):
        # inner layer do action
        def wrap(request, *args, **kwargs):
            if check_privilege(request.user, perm_code):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied
        return wrap
    return decorator


def check_privilege(user, perm_code):
    if isinstance(perm_code, str):
        return user.has_perm(perm_code) or user.has_module_perms(perm_code)
    elif isinstance(perm_code, list):
        return user.has_perms(perm_code)
    else:
        return False
