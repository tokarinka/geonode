from geonode.tests.base import GeoNodeBaseTestSupport
from unittest.mock import MagicMock
from django.test import TestCase

import requests
from urllib.parse import urljoin
from django.core.exceptions import ObjectDoesNotExist

from geonode.groups.models import GroupProfile
from .models import KeycloakRole
from . import helper

def _log(msg, *args):
    logger.debug(msg, *args)

class KeycloakRoleTest(GeoNodeBaseTestSupport):

    def setUp(self):
        self.group_test = GroupProfile.objects.create(title='test 1', slug='test1', description='test1')
        KeycloakRole.objects.create(keycloak_id='test1', name='test 1', group=self.group_test)
    
    def test_keycloak_role_exists(self):
        role = KeycloakRole.objects.get(keycloak_id='test1')

        self.assertEqual('test1', role.keycloak_id)
    
    def test_creating_keycloak_role_with_non_existing_group(self):
        try:
            role_is_none = KeycloakRole.objects.get(keycloak_id='test2')
        except KeycloakRole.DoesNotExist:
            role_is_none = None
        
        self.assertEqual(None, role_is_none)

        group_test2 = GroupProfile.objects.create(title='test 2', slug='test2', description='test2')
        KeycloakRole.objects.create(keycloak_id='test2', name='test 2', group=group_test2)
        role = KeycloakRole.objects.get(keycloak_id='test2')

        self.assertEqual('test2', role.keycloak_id)

    def test_creating_keycloak_role_with_existing_group(self):
        KeycloakRole.objects.filter(keycloak_id='test1').delete()

        KeycloakRole.objects.create(keycloak_id='test1', name='test 1', group=self.group_test)
        role = KeycloakRole.objects.get(keycloak_id='test1')

        self.assertEqual(self.group_test, role.group)

    def test_delete_role_leads_to_group_still_existing(self):
        group_test3 = GroupProfile.objects.create(title='test 3', slug='test3', description='test3')
        KeycloakRole.objects.create(keycloak_id='test3', name='test 3', group=group_test3)

        KeycloakRole.objects.filter(keycloak_id='test3').delete()
        group = GroupProfile.objects.get(slug='test3')

        self.assertEqual('test3', group.slug)

    def test_deleting_group_leads_to_deletion_of_role(self):
        GroupProfile.objects.filter(slug='test1').delete()

        try:
            role_is_none = KeycloakRole.objects.get(keycloak_id='test1')
        except KeycloakRole.DoesNotExist:
            role_is_none = None
        
        self.assertEqual(None, role_is_none)

class KeycloakRequestMockTest(TestCase):
    
    def test_get_token(self):
        helper.get_request = MagicMock(return_value={'access_token':'TOKEN'})
        assert helper.get_request('POST', 'url', 'data') == {'access_token':'TOKEN'}
        assert helper.get_token('client', 'secret', 'grant', 'scope') == 'TOKEN'

    def test_get_roles(self):
        helper.get_request = MagicMock(return_value={'keycloak_id':'KEYCLOAK'})
        assert helper.get_request('GET', 'url', 'header') == {'keycloak_id':'KEYCLOAK'}
        assert helper.get_roles('realm', 'client-id', 'token') == {'keycloak_id':'KEYCLOAK'}