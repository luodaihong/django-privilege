# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import User as DjangoUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _

from privilege.core.config import ACCESSIBLE_APPS


ACCESSIBLE_CONTENT_TYPES = ContentType.objects.filter(app_label__in=ACCESSIBLE_APPS)


__all__ = ['GroupForm', 'PermissionForm', 'UserCreateForm', 'ResetPasswordForm']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name", )


class PermissionForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(label=_("Target Objects"), queryset=ACCESSIBLE_CONTENT_TYPES, empty_label=None,
                                          help_text=_("Choose which object your permission will work on."))
    codename = forms.CharField(label=_("codename"), max_length=100,
                               help_text=_("Input add_xxx, the final permission_code will be privilege.add_xxx"))

    class Meta:
        model = Permission

    def clean_codename(self):
        codename = self.cleaned_data["codename"]
        if codename.find("privilege.") == 0:
            raise forms.ValidationError(_("Forbid code starting with 'privilege.' to avoid mistake"))
        return codename


class UserCreateForm(UserCreationForm):
    class Meta:
        model = DjangoUser
        fields = ("username", "email",)


class ResetPasswordForm(SetPasswordForm):
    pass
