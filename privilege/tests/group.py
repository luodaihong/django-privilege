# -*- coding: UTF-8 -*-

from django.test import Client, TestCase
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import simplejson

from privilege.core.config import GROUP_CACHE_KEY


class GroupTestCases(TestCase):
    fixtures = ['privilege.json']

    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()

    def tearDown(self):
        self.client.logout()
        TestCase.tearDown(self)


    def test_group_list_not_login(self):
        group_list_url = reverse("privilege.views.group.group_list", args=(1, ))
        self.check_not_login(group_list_url)

    def test_group_list_logined_but_not_superuser(self):
        group_list_url = reverse("privilege.views.group.group_list", args=(1, ))
        self.check_not_superuser(group_list_url)

    def test_group_list_ok(self):
        group_list_url = reverse("privilege.views.group.group_list", args=(1, ))
        self.client.login(username="super", password="test")
        response = self.client.get(group_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["page"].object_list)


    def test_group_detail_not_login(self):
        group_detail_url = reverse("privilege.views.group.group_detail", args=(1, 1,))
        self.check_not_login(group_detail_url)

    def test_get_group_detail_logined_but_not_superuser(self):
        group_detail_url = reverse("privilege.views.group.group_detail", args=(1, 1,))
        self.check_not_superuser(group_detail_url)

    def test_get_group_detail_not_exist(self):
        group_detail_url = reverse("privilege.views.group.group_detail", args=(0, 1,))
        self.client.login(username="super", password="test")
        response = self.client.get(group_detail_url)
        self.assertEqual(response.status_code, 404)

    def test_get_group_detail_ok(self):
        group_detail_url = reverse("privilege.views.group.group_detail", args=(1, 1,))
        self.client.login(username="super", password="test")
        response = self.client.get(group_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["group"])


    def test_change_group_permission_not_login(self):
        change_group_url = reverse("privilege.views.group.change_group_permission")
        self.check_not_login(change_group_url)

    def test_change_group_permission_not_super_user(self):
        change_group_url = reverse("privilege.views.group.change_group_permission")
        self.check_not_superuser(change_group_url)

    def test_change_group_permission_get_method(self):
        change_group_url = reverse("privilege.views.group.change_group_permission")
        self.client.login(username="super", password="test")
        response = self.client.get(change_group_url)
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "nok", "msg": _("Fail")})
        self.assertEqual(response.content, expect_content)

    def test_change_group_permission_not_exist(self):
        change_group_url = reverse("privilege.views.group.change_group_permission")
        post_data = {"group_id": 0}
        self.client.login(username="super", password="test")
        response = self.client.post(change_group_url, post_data)
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "nok", "msg": _("Fail")})
        self.assertEqual(response.content, expect_content)

    def test_change_group_permission_post_bad_params(self):
        change_group_url = reverse("privilege.views.group.change_group_permission")
        post_data = {"group_id": 1, "permission_id": ""}
        self.client.login(username="super", password="test")
        response = self.client.post(change_group_url, post_data)
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "nok", "msg": _("Fail")})
        self.assertEqual(response.content, expect_content)

    def test_change_group_permission_ok(self):
        change_group_url = reverse("privilege.views.group.change_group_permission")
        post_data = {"group_id": 1, "permission_id": "1", "op_code": "add"}
        self.client.login(username="super", password="test")
        response = self.client.post(change_group_url, post_data)
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "ok", "msg": _("Success")})
        self.assertEqual(response.content, expect_content)
        cache.set(GROUP_CACHE_KEY, None)


    def test_add_group_not_login(self):
        add_group_url = reverse("privilege.views.group.add_group")
        self.check_not_login(add_group_url)

    def test_add_group_not_superuser(self):
        add_group_url = reverse("privilege.views.group.add_group")
        self.check_not_superuser(add_group_url)

    def test_add_group_not_post(self):
        add_group_url = reverse("privilege.views.group.add_group")
        self.client.login(username="super", password="test")
        response = self.client.get(add_group_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"])

    def test_add_group_post_blank(self):
        add_group_url = reverse("privilege.views.group.add_group")
        self.client.login(username="super", password="test")
        response = self.client.post(add_group_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_add_group_ok(self):
        add_group_url = reverse("privilege.views.group.add_group")
        self.client.login(username="super", password="test")
        response = self.client.post(add_group_url, {"name": "add_success"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Group.objects.filter(name="add_success").count())
        Group.objects.filter(name="add_success").delete()
        cache.set(GROUP_CACHE_KEY, None)


    def test_edit_group_not_login(self):
        edit_group_url = reverse("privilege.views.group.edit_group", args=(1, ))
        self.check_not_login(edit_group_url)

    def test_edit_group_not_superuser(self):
        edit_group_url = reverse("privilege.views.group.edit_group", args=(1, ))
        self.check_not_superuser(edit_group_url)

    def test_test_edit_group_not_exist(self):
        edit_group_url = reverse("privilege.views.group.edit_group", args=(0, ))
        self.client.login(username="super", password="test")
        response = self.client.get(edit_group_url)
        self.assertEqual(response.status_code, 404)

    def test_test_edit_group_not_post(self):
        edit_group_url = reverse("privilege.views.group.edit_group", args=(1, ))
        self.client.login(username="super", password="test")
        response = self.client.get(edit_group_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"])

    def test_test_edit_group_post_blank(self):
        edit_group_url = reverse("privilege.views.group.edit_group", args=(1, ))
        self.client.login(username="super", password="test")
        response = self.client.post(edit_group_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_test_edit_group_ok(self):
        group = Group.objects.create(name="to_delete")
        edit_group_url = reverse("privilege.views.group.edit_group", args=(group.id, ))
        self.client.login(username="super", password="test")
        response = self.client.post(edit_group_url, {"name": "changed"})
        self.assertEqual(response.status_code, 302)
        group = Group.objects.get(id=group.id)
        self.assertEqual(group.name, "changed")
        group.delete()
        cache.set(GROUP_CACHE_KEY, None)


    def test_delete_grooup_not_login(self):
        delete_group_url = reverse("privilege.views.group.delete_group", args=(1, ))
        self.check_not_login(delete_group_url)

    def test_delete_grooup_not_superuser(self):
        delete_group_url = reverse("privilege.views.group.delete_group", args=(1, ))
        self.check_not_superuser(delete_group_url)

    def test_delete_grooup_ok(self):
        delete_group_url = reverse("privilege.views.group.delete_group", args=(0, ))
        response = self.client.post(delete_group_url)
        self.assertEqual(response.status_code, 302)
        cache.set(GROUP_CACHE_KEY, None)


    def check_not_login(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def check_not_superuser(self, url):
        self.client.login(username="test", password="test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
