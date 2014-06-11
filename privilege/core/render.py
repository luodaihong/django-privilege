# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings


def render_json(view_func):
    def wrap(request, *args, **kwargs):
        return_value = view_func(request, *args, **kwargs)

        if isinstance(return_value, HttpResponse):
            return_value.mimetype = 'application/json'
            response = return_value
        else:
            json = simplejson.dumps(return_value)
            response = HttpResponse(json, mimetype='application/json')

        response['Cache-Control'] = 'no-cache'
        return response
    return wrap


def render_template(template, request, **kwargs):
    new_kwargs = {"settings": settings}
    if "settings" in kwargs:
        kwargs.pop("settings")
    if request is not None:
        kwargs["request"] = request
    new_kwargs.update(kwargs)

    if request is not None:
        instance = RequestContext(request)
        return render_to_response(template, new_kwargs, context_instance=instance)

    return render_to_response(template, new_kwargs)
