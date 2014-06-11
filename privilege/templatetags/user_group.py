# -*- coding: utf-8 -*-

from django import template
from django.contrib.auth.models import User as DjangoUser

register = template.Library()


@register.inclusion_tag("tags/user_group.html", name="user_group")
def render_new_users(group, number, **kwargs):
    """render users by group"""
    users = DjangoUser.objects.only("id", "username").filter(groups=group).order_by("-id")[0:number]
    return {"users": users, "group": group}
