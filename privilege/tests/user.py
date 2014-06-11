# -*- coding: UTF-8 -*-

from django.test import Client, TestCase
from django.contrib.auth.models import User as DjangoUser
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.translation import ugettext as _


class UserTestCases(TestCase):
    fixtures = ['privilege.json']

    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()

    def tearDown(self):
        self.client.logout()
        TestCase.tearDown(self)


    def test_switch_active_user_not_login(self):
        forbid_user_url = reverse("privilege.views.user.switch_active_user", args=(1, ))
        self.check_not_login(forbid_user_url)

    def test_switch_active_user_not_superuser(self):
        forbid_user_url = reverse("privilege.views.user.switch_active_user", args=(1, ))
        self.check_not_superuser(forbid_user_url)

    def test_switch_active_user_not_exists(self):
        forbid_user_url = reverse("privilege.views.user.switch_active_user", args=(0, ))
        self.client.login(username="super", password="test")
        response = self.client.get(forbid_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "nok", "msg": _("User does not exist.")}
        self.assertEqual(simplejson.loads(response.content), expect_content)

    def test_switch_active_user_ok(self):
        forbid_user_url = reverse("privilege.views.user.switch_active_user", args=(6, ))
        self.client.login(username="super", password="test")

        response = self.client.get(forbid_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "ok", "msg": _("Forbid ok"), "current": False}
        self.assertEqual(simplejson.loads(response.content), expect_content)
        user = DjangoUser.objects.get(id=6)
        self.assertFalse(user.is_staff)

        response = self.client.get(forbid_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "ok", "msg": _("Activate ok"), "current": True}
        self.assertEqual(simplejson.loads(response.content), expect_content)
        user = DjangoUser.objects.get(id=6)
        self.assertTrue(user.is_staff)


    def test_switch_super_user_not_login(self):
        switch_super_user_url = reverse("privilege.views.user.switch_super_user", args=(5, ))
        self.check_not_login(switch_super_user_url)

    def test_switch_super_user_not_superuser(self):
        switch_super_user_url = reverse("privilege.views.user.switch_super_user", args=(5, ))
        self.check_not_superuser(switch_super_user_url)

    def test_switch_super_user_not_exists(self):
        switch_super_user_url = reverse("privilege.views.user.switch_super_user", args=(0, ))
        self.client.login(username="super", password="test")
        response = self.client.get(switch_super_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "nok", "msg": _("User does not exist.")}
        self.assertEqual(simplejson.loads(response.content), expect_content)

    def test_switch_super_user_myself(self):
        switch_super_user_url = reverse("privilege.views.user.switch_super_user", args=(6, ))
        self.client.login(username="super", password="test")
        response = self.client.get(switch_super_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "nok", "msg": _("The target cannot be yourself.")}
        self.assertEqual(simplejson.loads(response.content), expect_content)

    def test_switch_super_user_ok(self):
        switch_super_user_url = reverse("privilege.views.user.switch_super_user", args=(5, ))
        self.client.login(username="super", password="test")
        response = self.client.get(switch_super_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "ok", "msg": _("Root success"), "current": True}
        self.assertEqual(simplejson.loads(response.content), expect_content)
        user = DjangoUser.objects.get(id=5)
        self.assertTrue(user.is_superuser)

        response = self.client.get(switch_super_user_url)
        self.assertEqual(response.status_code, 200)
        expect_content = {"status": "ok", "msg": _("UnRoot success"), "current": False}
        self.assertEqual(simplejson.loads(response.content), expect_content)
        user = DjangoUser.objects.get(id=5)
        self.assertFalse(user.is_superuser)


    def test_user_list_not_login(self):
        users_permissions_url = reverse("privilege.views.user.user_list", args=(1,))
        self.check_not_login(users_permissions_url)

    def test_user_list_not_superuser(self):
        users_permissions_url = reverse("privilege.views.user.user_list", args=(1,))
        self.check_not_superuser(users_permissions_url)

    def test_user_list_ok(self):
        users_permissions_url = reverse("privilege.views.user.user_list", args=(1,))
        self.client.login(username="super", password="test")
        response = self.client.get(users_permissions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["permissions"] is not None)


    def test_change_user_permission_not_login(self):
        chang_permission_url = reverse("privilege.views.user.change_user_permission")
        self.check_not_login(chang_permission_url)

    def test_change_user_permission_not_super(self):
        chang_permission_url = reverse("privilege.views.user.change_user_permission")
        self.check_not_superuser(chang_permission_url)

    def test_change_user_permission_not_post(self):
        chang_permission_url = reverse("privilege.views.user.change_user_permission")
        self.client.login(username="super", password="test")
        response = self.client.get(chang_permission_url)
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "nok", "msg": _("Fail")})
        self.assertEqual(response.content, expect_content)

    def test_change_user_permission_user_not_exist(self):
        chang_permission_url = reverse("privilege.views.user.change_user_permission")
        self.client.login(username="super", password="test")
        response = self.client.post(chang_permission_url, {"user_id": 0})
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "nok", "msg": _("Fail")})
        self.assertEqual(response.content, expect_content)

    def test_change_user_permission_bad_params(self):
        chang_permission_url = reverse("privilege.views.user.change_user_permission")
        self.client.login(username="super", password="test")
        post_data = {"user_id": 5, "op_code": "aaa", "param_type": "group", "param_id": 1}
        response = self.client.post(chang_permission_url, post_data)
        self.assertEqual(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "nok", "msg": _("Unknown param op_code.")})
        self.assertEqual(response.content, expect_content)

    def test_change_user_permission_ok(self):
        chang_permission_url = reverse("privilege.views.user.change_user_permission")
        self.client.login(username="super", password="test")
        post_data = {"user_id": 5, "op_code": "add", "param_type": "group", "param_id": 1}
        response = self.client.post(chang_permission_url, post_data)
        self.assertTrue(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "ok", "msg": _("Success")})
        self.assertEqual(response.content, expect_content)

        post_data = {"user_id": 5, "op_code": "add", "param_type": "permission", "param_id": 1}
        response = self.client.post(chang_permission_url, post_data)
        self.assertTrue(response.status_code, 200)
        expect_content = simplejson.dumps({"status": "ok", "msg": _("Success")})
        self.assertEqual(response.content, expect_content)


    def test_search_not_login(self):
        search_url = reverse("privilege.views.user.search", args=(1,))
        self.check_not_login(search_url)

    def test_search_not_super(self):
        search_url = reverse("privilege.views.user.search", args=(1,))
        self.check_not_superuser(search_url)

    def test_search_post_blank(self):
        search_url = reverse("privilege.views.user.search", args=(1,))
        self.client.login(username="super", password="test")
        response = self.client.post(search_url)
        self.assertEqual(response.status_code, 302)

    def test_search_ok(self):
        search_url = reverse("privilege.views.user.search", args=(1,))
        self.client.login(username="super", password="test")
        response = self.client.post(search_url, {"keyword": "s"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page"].object_list), 2)


    def test_add_user_not_login(self):
        add_user_url = reverse("privilege.views.user.add_user")
        self.check_not_login(add_user_url)

    def test_add_user_not_super(self):
        add_user_url = reverse("privilege.views.user.add_user")
        self.check_not_superuser(add_user_url)

    def test_add_user_not_post(self):
        self.client.login(username="super", password="test")
        add_user_url = reverse("privilege.views.user.add_user")
        response = self.client.get(add_user_url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.errors)

    def test_add_user_ok(self):
        add_user_url = reverse("privilege.views.user.add_user")
        self.client.login(username="super", password="test")
        post_data = {"username": "987654321", "email": "987654321@funshion.com",
                     "password1": "987654321", "password2": "987654321"}
        response = self.client.post(add_user_url, post_data)
        self.assertEqual(response.status_code, 302)


    def test_reset_user_password_not_login(self):
        reset_user_url = reverse("privilege.views.user.reset_user_password", args=(5,))
        self.check_not_login(reset_user_url)

    def test_reset_user_password_not_super(self):
        reset_user_url = reverse("privilege.views.user.reset_user_password", args=(5,))
        self.check_not_superuser(reset_user_url)

    def test_reset_user_password_not_exist(self):
        reset_user_url = reverse("privilege.views.user.reset_user_password", args=(0,))
        self.client.login(username="super", password="test")
        response = self.client.post(reset_user_url)
        self.assertEqual(response.status_code, 404)

    def test_reset_user_password_not_post(self):
        reset_user_url = reverse("privilege.views.user.reset_user_password", args=(5,))
        self.client.login(username="super", password="test")
        response = self.client.get(reset_user_url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.errors)


    def test_reset_user_password_ok(self):
        reset_user_url = reverse("privilege.views.user.reset_user_password", args=(5,))
        self.client.login(username="super", password="test")
        post_data = {"user_id": 5, "new_password1": "987654321", "new_password2": "987654321"}
        response = self.client.post(reset_user_url, post_data)
        self.assertEqual(response.status_code, 302)


    def check_not_login(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def check_not_superuser(self, url):
        self.client.login(username="test", password="test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
