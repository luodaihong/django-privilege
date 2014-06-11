# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.http import Http404

from privilege.forms import UserCreateForm, ResetPasswordForm
from privilege.core.config import SITE_NAME, PRIVILEGE_PAGE_SIZE, LEFT_MENUS, ACTIVE_WHEN_ADDED
from privilege.core.render import render_template, render_json
from privilege.core.pagination import get_page
from privilege.core.cache_utils import get_latest_groups, get_latest_permissions
from privilege.core.decorator import required_superuser


CURRENT_MENU = _("User Center")


@render_json
@required_superuser
def switch_active_user(request, userid):
    """turn is_staff and is_active to True/False"""
    result = {"status": "ok"}

    try:
        user = DjangoUser.objects.get(id=userid)
        if user.is_staff or user.is_active:
            user.is_staff = False
            user.is_active = False
            result["msg"] = _("Forbid ok")
            result["current"] = False
        else:
            user.is_staff = True
            user.is_active = True
            result["msg"] = _("Activate ok")
            result["current"] = True
        user.save()
    except ObjectDoesNotExist:
        result["status"] = "nok"
        result["msg"] = _("User does not exist.")
    except Exception, e:
        result["status"] = "nok"
        result["msg"] = _("System error.")
        logging.error(e)

    return result


@render_json
@required_superuser
def switch_super_user(request, userid):
    """turn is_superuser to True/False"""
    if request.user.id == int(userid):
        return {"status": "nok", "msg": _("The target cannot be yourself.")}

    result = {"status": "ok"}
    try:
        user = DjangoUser.objects.get(id=userid)
        if user.is_superuser:
            user.is_superuser = False
            result["current"] = False
            result["msg"] = _("UnRoot success")
        else:
            user.is_superuser = True
            result["current"] = True
            result["msg"] = _("Root success")
        user.save()
    except ObjectDoesNotExist:
        result["status"] = "nok"
        result["msg"] = _("User does not exist.")
    except Exception, e:
        result["status"] = "nok"
        result["msg"] = _("System error.")
        logging.error(e)

    return result


@required_superuser
def user_list(request, pageno=1, pagesize=PRIVILEGE_PAGE_SIZE):
    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {'name': _("User Center")}
    ]

    users = DjangoUser.objects.only("id", "username", "is_staff").all()
    page = get_page(users, pageno, pagesize)
    groups = get_latest_groups()
    permissions = get_latest_permissions()
    url_prefix = reverse("privilege.views.user.user_list", args=(1, )).rstrip("/")[:-2]

    return render_template("privilege/user_list.html", page_title=breadcrumb[-1]["name"], 
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS, **locals())


@render_json
@required_superuser
def change_user_permission(request):
    result = {"status": "nok", "msg": ""}

    try:
        user_id = long(request.POST["user_id"])
        param_type = request.POST["param_type"]
        param_id = long(request.POST["param_id"])
        op_code = request.POST["op_code"]

        if op_code not in ["add", "delete"]:
            result["msg"] = _("Unknown param op_code.")
            return result

        user = DjangoUser.objects.get(id=user_id)
        if param_type == "group":
            group = Group.objects.get(id=param_id)
            if op_code == "add":
                user.groups.add(group)
            else:
                user.groups.remove(group)
        elif param_type == "permission":
            permission = Permission.objects.get(id=param_id)
            if op_code == "add":
                user.user_permissions.add(permission)
            else:
                user.user_permissions.remove(permission)
        else:
            result["msg"] = _("Unknown param type.")

        result["msg"] = _("Success")
        result["status"] = "ok"
    except Exception, e:
        logging.error(e)
        result["msg"] = _("Fail")

    return result


@required_superuser
def search(request, pageno=1, pagesize=PRIVILEGE_PAGE_SIZE):
    default_redirect = reverse("privilege.views.group.group_list", args=(1,))
    keyword, source_url = _get_keyword_source_url(request)

    if not keyword or not source_url:
        return redirect(default_redirect)

    if source_url.find("group") > 0:
        objlist = Group.objects.filter(name__contains=keyword)
        template = "privilege/group_list.html"
        current_menu = _("Group Center")
    else:
        objlist = DjangoUser.objects.filter(username__contains=keyword)
        template = "privilege/user_list.html"
        current_menu = _("User Center")
    page = get_page(objlist, pageno, pagesize)

    url_prefix = reverse("privilege.views.user.search", args=(1, )).rstrip("/")[:-2]
    groups = get_latest_groups()
    permissions = get_latest_permissions()
    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {"name": u"Search'%s'" % keyword}
    ]

    return render_template(page_title=breadcrumb[-1]["name"], CURRENT_MENU=current_menu,
                           LEFT_MENUS=LEFT_MENUS, **locals())


def _get_keyword_source_url(request):
    keyword = request.POST.get("keyword", "")
    if keyword:
        request.session['keyword'] = keyword
    else:
        keyword = request.session.get('keyword', "")

    source_url = request.META.get('HTTP_REFERER', '/')
    if source_url.find("search") > 0 or source_url.find("permission") > 0:  # 不是搜索用户或组
        source_url = request.session.get('source_url', "")
    else:
        request.session['source_url'] = source_url

    return (keyword, source_url)


@required_superuser
def add_user(request):
    user_list_url = reverse("privilege.views.user.user_list", args=(1,))
    if request.method == "POST":
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = ACTIVE_WHEN_ADDED
            user.is_active = ACTIVE_WHEN_ADDED
            user.save()
            return redirect(user_list_url)
    else:
        form = UserCreateForm()

    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {"name": _("User Center"), "url": user_list_url},
        {"name": _("Add User")}
    ]
    return render_template("privilege/user_add.html", button=_("Add"), page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS, **locals())


@required_superuser
def reset_user_password(request, userid):
    try:
        user = DjangoUser.objects.get(id=userid)
    except ObjectDoesNotExist:
        raise Http404

    user_list_url = reverse("privilege.views.user.user_list", args=(1,))

    if request.method == "POST":
        form = ResetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(user_list_url)
    else:
        form = ResetPasswordForm(user=user)

    breadcrumb = [
        {"name": SITE_NAME, "url": "/"},
        {"name": _("Permission Center"), "url": reverse("privilege.views.permission.permission_list")},
        {"name": _("User Center"), "url": user_list_url},
        {"name": _(u"Reset password")}
    ]
    return render_template("privilege/user_add.html", button=_("Change"), page_title=breadcrumb[-1]["name"],
                           CURRENT_MENU=CURRENT_MENU, LEFT_MENUS=LEFT_MENUS, **locals())
