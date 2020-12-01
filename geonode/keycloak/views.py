from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required

from .models import KeycloakRole
from .helper import get_token, get_roles
from geonode.groups.models import GroupProfile

# Synchronizes the keycloak roles with group profiles.
# Creates new instances of keycloak roles and assigns a profile group to each role.
# If the group does not exists new group will be created.
# If the  keycloak role already exists, it wont be created.
@staff_member_required
def synchronize_roles(request):
    client = 'geonode'
    client_secret = 'b8396cf3-f524-4e52-9dc9-f42e25f2d055'
    grant_type = 'client_credentials'
    scope = 'openid roles'
    token = get_token(client, client_secret, grant_type, scope) # Retrieves the token from keycloak.

    realm = 'master'
    client_id = 'bb1f0c0c-67fb-45b1-826f-726cf6162484'
    roles = get_roles(realm, client_id, token) # Retrieves the roles from keycloak.

    for role in roles: # Traverses through each role.
        group, _ = GroupProfile.objects.get_or_create(title=role["name"], slug=role["name"], description= role.get("description", ""))

        try:
            KeycloakRole.objects.get(keycloak_id=role["id"])
        except KeycloakRole.DoesNotExist:
            KeycloakRole.objects.create(keycloak_id=role["id"], name=role["name"], group=group)
    
    return redirect('/en/admin/keycloak-role/keycloakrole/')

    