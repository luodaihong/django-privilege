# -*- coding: utf-8 -*-

import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       )

#apps
urlpatterns += patterns('',
                        url(r'^privilege/', include("privilege.urls")),
                        )
