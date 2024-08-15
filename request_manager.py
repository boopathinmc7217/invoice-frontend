import requests

from config import AppConfig

class RequestManager:
    BASE_URL = 'http://127.0.0.1:8000/api/'

    def __init__(self):
        self.session = requests.Session()
        self.token = None  # Initialize token

    def set_token(self, token):
        self.token = token

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.BASE_URL}{endpoint}"
        if endpoint!="login/":
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = f'Bearer {AppConfig().get_jwt_token_access()}'
            kwargs['headers'] = headers
        response = self.session.request(method, url, **kwargs)
        self._handle_response(response)
        return response

    def _handle_response(self, response):
        if response.status_code >= 400:
            print(f"Error {response.status_code}: {response.text}")
        else:
            print(f"Success {response.status_code}: {response.text}")

    def get(self, endpoint, params=None):
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint=None, json=None, data=None):
        return self._request('POST', endpoint, json=json, data=data)

    def put(self, endpoint, json=None, data=None):
        return self._request('PUT', endpoint, json=json, data=data)

    def delete(self, endpoint):
        return self._request('DELETE', endpoint)
