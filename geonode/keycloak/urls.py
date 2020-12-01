from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path(
        'synchronize_roles',
        views.synchronize_roles,
        name='synchronize_roles'
    ),
]