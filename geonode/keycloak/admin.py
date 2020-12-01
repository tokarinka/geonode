from django.contrib import admin

from .models import KeycloakRole

class KeycloakAdmin(admin.ModelAdmin):
    model = KeycloakRole

admin.site.register(KeycloakRole, KeycloakAdmin)