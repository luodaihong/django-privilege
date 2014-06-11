# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.template import TemplateSyntaxError


register = template.Library()


@register.tag("breadcrumb")
def do_breadcrumb(parser, token):
    try:
        _, breadcrumb, request = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return BreadcrumbNode(breadcrumb, request)


class BreadcrumbNode(template.Node):
    def __init__(self, breadcrumb, request):
        self.breadcrumb = template.Variable(breadcrumb)
        self.request = template.Variable(request)

    def render(self, context):
        t = template.loader.get_template("tags/breadcrumb.html")
        new_context = Context({'breadcrumb': self.breadcrumb.resolve(context),
                               'request': self.request.resolve(context)},
                              autoescape=context.autoescape)
        return t.render(new_context)


@register.tag("vertical_nav")
def do_vertical_nav(parser, token):
    try:
        _, tab, tabs = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return VerticalNavNode(tab, tabs)


class VerticalNavNode(template.Node):
    def __init__(self, tab, tabs):
        self.tab = template.Variable(tab)
        self.tabs = template.Variable(tabs)

    def render(self, context):
        t = template.loader.get_template("tags/vertical_nav.html")
        tabs = self.tabs.resolve(context)
        cur_tab = self.tab.resolve(context)
        new_context = Context({'cur_tab': cur_tab, 'tabs': tabs},
                              autoescape=context.autoescape)
        return t.render(new_context)
