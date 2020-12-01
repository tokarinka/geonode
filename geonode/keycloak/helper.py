import requests
from urllib.parse import urljoin

BASE_URL = 'http://keycloak:8080'

# get_request creates and executes the request.
# Returns a json response.
def get_request(request_type, **kwargs):    
    if request_type == 'POST':
        resp = requests.post(**kwargs).json()
    elif request_type == 'GET':
        resp = requests.get(**kwargs).json()

    return resp

# get_token intakes required fields to build the periemters for data,
# constructs the url and the retrieves the response from get_request.
# Returns the access token.
def get_token(client_id, client_secret, grant_type, scope):
    url = f'{BASE_URL}/auth/realms/master/protocol/openid-connect/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': grant_type,
        'scope': scope,
    }

    resp = get_request('POST', url=url, data=data)

    return resp["access_token"]
    
# get_roles intakes required fields to build the header of the request,
# constructs the url and retrives the response from get_request.
# Returns a dictionary of keycloak roles. 
def get_roles(realm, client_id, token):
    url = f'{BASE_URL}/auth/admin/realms/{realm}/clients/{client_id}/roles'
    headers = {
        "Authorization": f'Bearer {token}',
    }

    resp = get_request('GET', url=url, headers=headers)

    return resp