# -*-  coding: UTF-8

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


__all__ = ['IsolatedIsland', ]


class IsolatedIsland(models.Model):
    """As the model name mentioned, no views function will CRUD this model.
    It just creates a ContentType instance that will be used for custom permission.
    This custom permission may work on zero or multiple models at the same time.
    """
    app_name = models.CharField(u"APP名", max_length=32)

    class Meta:
        app_label = "privilege"
        verbose_name = _("Custom Permission")
        verbose_name_plural = _("Custom Permission")

    def __unicode__(self):
        return smart_unicode("%s" % (self.app_name))
