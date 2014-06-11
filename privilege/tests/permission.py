# -*- coding: UTF-8 -*-

from django.test import Client, TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.cache import cache

from privilege.core.config import PERMISSION_CACHE_KEY, ACCESSIBLE_APPS


class PermissionTestCases(TestCase):
    fixtures = ['privilege.json']

    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()

    def tearDown(self):
        self.client.logout()
        TestCase.tearDown(self)


    def test_permission_list_not_login(self):
        permission_list_url = reverse("privilege.views.permission.permission_list")
        self.check_not_login(permission_list_url)

    def test_permission_list_not_superuser(self):
        permission_list_url = reverse("privilege.views.permission.permission_list")
        self.check_not_superuser(permission_list_url)

    def test_permission_list_ok(self):
        permission_list_url = reverse("privilege.views.permission.permission_list")
        self.client.login(username="super", password="test")
        response = self.client.get(permission_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["permissions"] is not None)


    def test_add_permission_not_login(self):
        add_permission_url = reverse("privilege.views.permission.add_permission")
        self.check_not_login(add_permission_url)

    def test_add_permission_not_superuser(self):
        add_permission_url = reverse("privilege.views.permission.add_permission")
        self.check_not_superuser(add_permission_url)

    def test_add_permission_not_post(self):
        add_permission_url = reverse("privilege.views.permission.add_permission")
        self.client.login(username="super", password="test")
        response = self.client.get(add_permission_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"])

    def test_add_permission_post_blank(self):
        add_permission_url = reverse("privilege.views.permission.add_permission")
        self.client.login(username="super", password="test")
        response = self.client.post(add_permission_url, {"name": "", "content_type": "", "codename": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_add_permission_ok(self):
        content_type_id = self.prepare_content_type()
        add_permission_url = reverse("privilege.views.permission.add_permission")
        self.client.login(username="super", password="test")
        response = self.client.post(add_permission_url, {"name": "add_test_cases", "content_type": content_type_id, "codename": "xxx"})
        if content_type_id:
            self.assertEqual(response.status_code, 302)
            new_permission = Permission.objects.filter(name="add_test_cases")
            self.assertTrue(new_permission.count())
            new_permission.delete()
            cache.set(PERMISSION_CACHE_KEY, None)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)


    def test_delete_permissions_not_login(self):
        delete_permission_url = reverse("privilege.views.permission.delete_permissions")
        self.check_not_login(delete_permission_url)

    def test_delete_permissions_not_superuser(self):
        delete_permission_url = reverse("privilege.views.permission.delete_permissions")
        self.check_not_superuser(delete_permission_url)

    def test_delete_permissions_balnk_string(self):
        delete_permission_url = reverse("privilege.views.permission.delete_permissions")
        self.client.login(username="super", password="test")
        response = self.client.post(delete_permission_url, {"permission": ""})
        self.assertEqual(response.status_code, 302)

    def test_delete_permissions_not_exists(self):
        delete_permission_url = reverse("privilege.views.permission.delete_permissions")
        self.client.login(username="super", password="test")
        response = self.client.post(delete_permission_url, {"permission": "-100"})
        self.assertEqual(response.status_code, 302)

    def test_delete_permissions_ok(self):
        delete_permission_url = reverse("privilege.views.permission.delete_permissions")
        self.client.login(username="super", password="test")
        response = self.client.post(delete_permission_url, {"permission": "100"})
        self.assertEqual(response.status_code, 302)
        delete_permission = Permission.objects.filter(id=100)
        self.assertFalse(delete_permission.count())
        cache.set(PERMISSION_CACHE_KEY, None)


    def test_change_permission_not_login(self):
        change_permission_url = reverse("privilege.views.permission.change_permission", args=(1, ))
        self.check_not_login(change_permission_url)

    def test_change_permission_not_super(self):
        change_permission_url = reverse("privilege.views.permission.change_permission", args=(1, ))
        self.check_not_superuser(change_permission_url)

    def test_change_permission_not_post(self):
        change_permission_url = reverse("privilege.views.permission.change_permission", args=(1, ))
        self.client.login(username="super", password="test")
        response = self.client.get(change_permission_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"])
        self.assertEqual(response.context["button"], _("Change"))

    def test_change_permission_post_blank(self):
        change_permission_url = reverse("privilege.views.permission.change_permission", args=(1, ))
        self.client.login(username="super", password="test")
        response = self.client.post(change_permission_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(response.context["button"], _("Change"))

    def test_change_permission_ok(self):
        content_type_id = self.prepare_content_type()
        change_permission_url = reverse("privilege.views.permission.change_permission", args=(1, ))
        self.client.login(username="super", password="test")
        post_data = {"name": "test", "content_type": content_type_id, "codename": "test"}
        response = self.client.post(change_permission_url, post_data)
        if content_type_id:
            self.assertEqual(response.status_code, 302)
            permission = Permission.objects.get(id=1)
            self.assertEqual(permission.name, "test")
            cache.set(PERMISSION_CACHE_KEY, None)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
            self.assertEqual(response.context["button"], _("Change"))


    def check_not_login(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def check_not_superuser(self, url):
        self.client.login(username="test", password="test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def prepare_content_type(self):
        try:
            content_type_id = ContentType.objects.filter(app_label__in=ACCESSIBLE_APPS)[0].id
        except:
            content_type_id = 0
        return content_type_id
