# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _


from privilege.forms import GroupForm
from privilege.core.config import SITE_NAME, PRIVILEGE_PAGE_SIZE, LEFT_MENUS
from privilege.core.render import render_template, render_json
from privilege.core.pagination import get_page
from privilege.core.cache_utils import get_latest_groups, update_groups, get_latest_permissions
from privilege.core.decorator import required_superuser


CURRENT_MENU = _("Group Center")


@required_superuser
def group_list(request, pageno=1, pagesize=PRIVILEGE_PAGE_SIZE):
    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {'name': _("Group Center")}
    ]
    groups = get_latest_groups()
    group_page = get_page(groups, pageno, pagesize)
    permissions = get_latest_permissions()
    url_prefix = reverse("privilege.views.group.group_list", args=(1, )).rstrip("/")[:-2]

    return render_template("privilege/group_list.html", request, page=group_page, breadcrumb=breadcrumb,
                           permissions=permissions, url_prefix=url_prefix, page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS)


@required_superuser
def group_detail(request, groupid, page_no=1, page_size=60):
    try:
        group = Group.objects.get(id=groupid)
        django_users = DjangoUser.objects.only("id", "username").filter(groups=group)
        user_page = get_page(django_users, page_no, page_size)
    except ObjectDoesNotExist:
        raise Http404

    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {"name": _("Group Center"), "url": reverse("privilege.views.group.group_list", args=(1,))},
        {'name': group.name}
    ]
    url_prefix = reverse("privilege.views.group.group_detail", args=(groupid, page_no, )).rstrip("/")[:-2]
    permissions = get_latest_permissions()

    return render_template("privilege/group_detail.html", request, group=group, breadcrumb=breadcrumb,
                           permissions=permissions, page=user_page, url_prefix=url_prefix,
                           page_title=breadcrumb[-1]["name"], CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS)


@render_json
@required_superuser
def change_group_permission(request):
    result = {"status": "nok", "msg": ""}

    try:
        permission_id = long(request.POST["permission_id"])
        group_id = long(request.POST["group_id"])
        op_code = request.POST["op_code"]

        if op_code not in ["add", "delete"]:
            result["msg"] = _("Unknown param op_code.")
            return result

        permission = Permission.objects.get(id=permission_id)
        group = Group.objects.get(id=group_id)
        if op_code == "add":
            group.permissions.add(permission)
        else:
            group.permissions.remove(permission)

        result["msg"] = _("Success")
        result["status"] = "ok"
    except Exception, e:
        logging.error(e)
        result["msg"] = _("Fail")

    return result


@required_superuser
def add_group(request):
    if request.method == "POST":
        form = GroupForm(data=request.POST)
        if form.is_valid():
            group = form.save()
            update_groups()
            return redirect(reverse("privilege.views.group.group_detail", args=(group.id, 1,)))
    else:
        form = GroupForm()

    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {"name": _("Group Center"), "url": reverse("privilege.views.group.group_list", args=(1,))},
        {'name': _("Add Group")}
    ]

    return render_template("privilege/group_add.html", request, breadcrumb=breadcrumb,
                           form=form, button=_("Add"), page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS)


@required_superuser
def edit_group(request, groupid):
    try:
        group = Group.objects.get(id=groupid)
    except:
        raise Http404

    if request.method == "POST":
        form = GroupForm(instance=group, data=request.POST)
        if form.is_valid():
            form.save()
            update_groups()
            return redirect(reverse("privilege.views.group.group_detail", args=(group.id, 1,)))
    else:
        form = GroupForm(instance=group)

    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {"name": _("Group Center"), "url": reverse("privilege.views.group.group_list", args=(1,))},
        {'name': _("Change Group")},
    ]

    return render_template("privilege/group_add.html", request, breadcrumb=breadcrumb,
                           form=form, button=_("Change"), page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS)


@required_superuser
def delete_group(request, groupid):
    try:
        Group.objects.get(id=groupid).delete()
        update_groups()
    except Exception, e:
        logging.error(e)
    return redirect(reverse("privilege.views.group.group_list", args=(1,)))
