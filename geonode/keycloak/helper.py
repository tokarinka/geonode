import requests
from urllib.parse import urljoin

BASE_URL = 'http://keycloak:8080'

def keycloak_get_token(client_id, client_secret, grant_type, scope):
    url = f'{BASE_URL}/auth/realms/master/protocol/openid-connect/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': grant_type,
        'scope': scope,
    }

    resp = requests.post(url = url, data = data).json()

    return resp["access_token"]
    

def keycloak_get_roles(realm, client_id, token):
    url = f'{BASE_URL}/auth/admin/realms/{realm}/clients/{client_id}/roles'
    headers = {
        "Authorization": f'Bearer {token}',
    }

    resp = requests.get(url = url, headers = headers).json()

    return resp