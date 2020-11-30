from geonode.tests.base import GeoNodeBaseTestSupport
from django.test import TestCase

import logging
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from . import views
from .models import KeycloakRole
from geonode.layers.models import Layer

logger = logging.getLogger(__name__)


def _log(msg, *args):
    logger.debug(msg, *args)

class KeycloakRoleTest(GeoNodeBaseTestSupport):

    def setUp(self):
        group_test = Group.objects.create(name='test 1')
        KeycloakRole.objects.create(keycloak_id='test1', name='test 1', group=group_test)

    def test_keycloak_role_exists(self):
        role = KeycloakRole.objects.get(keycloak_id='test1')
        self.assertEqual('test1', role.keycloak_id)

    def test_creating_keycloak_role(self):
        try:
            role_is_none = KeycloakRole.objects.get(keycloak_id='test2')
        except KeycloakRole.DoesNotExist:
            role_is_none = None
        
        self.assertEqual(None, role_is_none)

        group_test = Group.objects.create(name='test 2')
        KeycloakRole.objects.create(keycloak_id='test2', name='test 2', group=group_test)
        role = KeycloakRole.objects.get(keycloak_id='test2')
        self.assertEqual('test2', role.keycloak_id)

    def test_create_new_keycloak_role_group_not_exists(self):
        pass

    def test_create_new_keycloak_role_group_exists(self):
        pass

    def test_creating_keycloak_role_that_exists(self):
        pass

class HelperTest(TestCase):
    