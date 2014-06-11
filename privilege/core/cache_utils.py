# -*- coding: utf-8 -*-

from django.core.cache import cache
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from privilege.core.config import GROUP_CACHE_KEY, PERMISSION_CACHE_KEY


__all__ = ["update_permissions", "get_latest_permissions", "update_groups", "get_latest_groups"]


try:
    ACCESSIBLE_APPS = settings.ACCESSIBLE_APPS
except AttributeError:
    ACCESSIBLE_APPS = ["privilege"]
ACCESSIBLE_CONTENT_TYPES = ContentType.objects.filter(app_label__in=ACCESSIBLE_APPS)


def update_permissions():
    permissions = Permission.objects.filter(content_type__in=ACCESSIBLE_CONTENT_TYPES)\
        .exclude(codename__contains="isolatedisland").order_by("codename")
    cache.set(PERMISSION_CACHE_KEY, permissions)
    return permissions


def get_latest_permissions():
    permissions = cache.get(PERMISSION_CACHE_KEY)
    if not permissions:
        permissions = update_permissions()
    return permissions


def update_groups():
    groups = Group.objects.all().order_by("id")
    cache.set(GROUP_CACHE_KEY, groups)
    return groups


def get_latest_groups():
    groups = cache.get(GROUP_CACHE_KEY)
    if not groups:
        groups = update_groups()
    return groups
