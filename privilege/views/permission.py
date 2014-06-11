# -*- coding: utf-8 -*-

from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from privilege.forms import PermissionForm
from privilege.core.config import SITE_NAME, LEFT_MENUS
from privilege.core.render import render_template
from privilege.core.cache_utils import update_permissions, get_latest_permissions
from privilege.core.decorator import required_superuser


CURRENT_MENU = _("Permission Center")


@required_superuser
def permission_list(request):
    breadcrumb = [{"name": SITE_NAME, "url": "/"},
                  {"name": _("Permission Center")},
                  ]
    permissions = get_latest_permissions()

    return render_template("privilege/permission_list.html", page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS, **locals())


@required_superuser
def add_permission(request):
    if request.method == "POST":
        form = PermissionForm(data=request.POST)
        if form.is_valid():
            form.save()
            update_permissions()
            return redirect(reverse("privilege.views.permission.permission_list"))
    else:
        form = PermissionForm()

    breadcrumb = [{"name": SITE_NAME, "url": "/"},
                  {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
                  {"name": _("Add Permission")},
                  ]
    return render_template("privilege/permission_add.html", button=_("Add"), page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS, **locals())


@required_superuser
def delete_permissions(request):
    pids = request.REQUEST.getlist("permission")
    if request.method == "POST" and pids and pids != [u""]:
        Permission.objects.filter(id__in=pids).delete()
        update_permissions()

    return redirect(reverse("privilege.views.permission.permission_list"))


@required_superuser
def change_permission(request, pid):
    try:
        permission = Permission.objects.get(id=pid)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == "POST":
        form = PermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            update_permissions()
            return redirect(reverse("privilege.views.permission.permission_list"))
    else:
        form = PermissionForm(instance=permission)

    breadcrumb = [{"name": SITE_NAME, "url": "/"},
                  {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
                  {"name": _("Change Permission")},
                  ]

    return render_template("privilege/permission_add.html", button=_("Change"), page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS, **locals())
