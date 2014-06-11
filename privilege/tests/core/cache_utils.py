# -*- coding: UTF-8 -*-

from django.core.cache import cache
from django.test import TestCase

from privilege.core import cache_utils as utils
from privilege.core.config import GROUP_CACHE_KEY, PERMISSION_CACHE_KEY


class CacheUtilsTestCases(TestCase):
    fixtures = ['privilege.json']

    def test_update_permissions(self):
        utils.update_permissions()
        self.assertTrue(cache.get(PERMISSION_CACHE_KEY) is not None)
        cache.set(PERMISSION_CACHE_KEY, None)

    def test_get_latest_permissions(self):
        self.assertTrue(utils.get_latest_permissions() is not None)

    def test_update_groups(self):
        utils.update_groups()
        self.assertTrue(cache.get(GROUP_CACHE_KEY) is not None)
        cache.set(GROUP_CACHE_KEY, None)

    def test_get_latest_groups(self):
        self.assertTrue(utils.get_latest_groups() is not None)
