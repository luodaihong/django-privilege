# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


__all__ = ["LEFT_MENUS", "PRIVILEGE_PAGE_SIZE", "ACTIVE_WHEN_ADDED", "SITE_NAME",
           "ACCESSIBLE_APPS", "GROUP_CACHE_KEY", "PERMISSION_CACHE_KEY"]


LEFT_MENUS = [
    {"name": _("Permission Center"), "url": "/privilege/permission_list/"},
    {"name": _("Group Center"), "url": "/privilege/group_list/1/"},
    {"name": _("User Center"), "url": "/privilege/user_list/1/"},
]

try:
    PRIVILEGE_PAGE_SIZE = settings.PAGE_SIZE
except AttributeError:
    PRIVILEGE_PAGE_SIZE = 10

try:
    ACTIVE_WHEN_ADDED = settings.PAGE_SIZE
except AttributeError:
    ACTIVE_WHEN_ADDED = True

try:
    SITE_NAME = settings.SITE_NAME
except AttributeError:
    SITE_NAME = _("HomePage")

try:
    ACCESSIBLE_APPS = settings.ACCESSIBLE_APPS
except AttributeError:
    ACCESSIBLE_APPS = ["privilege"]


GROUP_CACHE_KEY, PERMISSION_CACHE_KEY = "privilege_groups", "privilege_permissions"
