# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('privilege.views',
    # APP home page
    url(r'^$', "permission.permission_list"),

    # actions for permission
    url(r'^permission_list/$', "permission.permission_list"),
    url(r'^add_permission/$', "permission.add_permission"),
    url(r'^change_permission/(?P<pid>\d+)/$', "permission.change_permission"),
    url(r'^delete_permissions/$', "permission.delete_permissions"),

    # actions for group
    url(r'^group_list/(?P<pageno>\d+)/$', "group.group_list"),
    url(r'^group_detail/(?P<groupid>\d+)/(?P<page_no>\d+)/$', "group.group_detail"),
    url(r'^add_group/$', "group.add_group"),
    url(r'^edit_group/(?P<groupid>\d+)/$', "group.edit_group"),
    url(r'^delete_group/(?P<groupid>\d+)/$', "group.delete_group"),
    url(r'^change_group_permission/$', "group.change_group_permission"),

    # actions for user
    url(r'^user_list/(?P<pageno>\d+)/$', "user.user_list"),
    url(r'^add_user/$', "user.add_user"),
    url(r'^switch_active_user/(?P<userid>\d+)/$', "user.switch_active_user"),
    url(r'^switch_super_user/(?P<userid>\d+)/$', "user.switch_super_user"),
    url(r'^reset_user_password/(?P<userid>\d+)/$', "user.reset_user_password"),
    url(r'^change_user_permission/$', "user.change_user_permission"),

    # search
    url(r'^search/(?P<pageno>\d+)/$', "user.search"),
)
