from django.apps import AppConfig

class KeycloakConfig(AppConfig):
    name = 'geonode.keycloak'
    label = 'keycloak-role'
    verbose_name = 'Keycloak' # Sets the display name within django administration.