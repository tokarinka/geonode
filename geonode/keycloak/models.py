from django.db import models
from django.contrib.auth.models import Group

from geonode.groups.models import GroupProfile

class KeycloakRole(models.Model):
    keycloak_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=50)
    group = models.OneToOneField(
        GroupProfile,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name + ' role'