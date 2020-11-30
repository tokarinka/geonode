from django.contrib import admin
from django.contrib.auth.models import Group

from . import helper
from .models import KeycloakRole
from geonode.groups.models import GroupProfile

def synchronize_roles(modeladmin, request, queryset):
    client = 'geonode'
    client_secret = 'b8396cf3-f524-4e52-9dc9-f42e25f2d055'
    grant_type = 'client_credentials'
    scope = 'openid roles'
    token = helper.keycloak_get_token(client, client_secret, grant_type, scope)

    realm = 'master'
    client_id = 'bb1f0c0c-67fb-45b1-826f-726cf6162484'
    roles = helper.keycloak_get_roles(realm, client_id, token)

    for role in roles:
        group, _ = Group.objects.get_or_create(name=role["name"])

        try:
            KeycloakRole.objects.get(name=role["name"])
        except KeycloakRole.MultipleObjectsReturned:
            pass
        except KeycloakRole.DoesNotExist:
            KeycloakRole.objects.create(keycloak_id=role["id"], name=role["name"], group=group)

synchronize_roles.short_description = "Synchronize Keycloak Roles"

class KeycloakAdmin(admin.ModelAdmin):
    actions = [synchronize_roles]

admin.site.register(KeycloakRole, KeycloakAdmin)