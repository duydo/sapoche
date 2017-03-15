import requests
from requests import HTTPError

from sapoche.helpers.preconditions import check_type

__author__ = 'duydo'


class JsonObject(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('%s has no property named %s.' % (self.__class__.__name__, name))

    def __setattr__(self, *args):
        raise AttributeError('%s instances are read-only.' % self.__class__.__name__)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))

    __delattr__ = __setitem__ = __delitem__ = __setattr__


class ApiException(Exception):
    def __init__(self, message=None, status=400):
        self.message = unicode(message)
        self.status = status
        super(ApiException, self).__init__(message)

    def __str__(self):
        return '<%s: %s>' % (self.status, self.message)


class ApiResponse(object):
    def __init__(self, status=200, data=None):
        self.status = status
        self.data = data

    def __repr__(self):
        return '<%s [%s]>' % (self.__class__.__name__, self.status)


class ApiPath(object):
    def __init__(self, api=None, path=None):
        self._api = check_type(api, Api)
        self._path = path

    def __getattr__(self, path):
        return self[path]

    def __getitem__(self, path):
        return self + ApiPath(self._api, path)

    def __add__(self, other):
        path = str(other)
        if self._path is not None:
            path = '%s/%s' % (self._path, path)
        return ApiPath(self._api, path)

    def __str__(self):
        return self._path

    def __repr__(self):
        return '<%s [%s]>' % (self.__class__.__name__, self._path)

    def get(self, params=None, **kwargs):
        """Send GET request.
        :param params: a dict of request params
        :return: see Api.__call__
        """
        return self._api('GET', self, params=params, **kwargs)

    def post(self, data=None, json=None, **kwargs):
        """Send POST request.
        :param data: (optional) dict, bytes or file-like object
        :param json: (optional) json data
        :return: see Api.__call__
        """
        return self._api('POST', self, data=data, json=json, **kwargs)

    def put(self, data=None, **kwargs):
        """Send PUT request.
        :param data: (optional) dict, bytes or file-like object
        :return: see Api.__call__
        """
        return self._api('PUT', self, data=data, **kwargs)

    def delete(self, **kwargs):
        """Send DELETE request."""
        return self._api('DELETE', self, **kwargs)


class Api(object):
    default_params = {}
    _session = None
    _base_url = None

    def __init__(self, base_url=None, session=None):
        self._base_url = base_url
        self._session = session or requests.Session()
        self._base_path = ApiPath(self, base_url)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __getattr__(self, path):
        if path.startswith(self._base_url):
            """This case happens when results have pagination"""
            return ApiPath(self, path)
        return self._base_path[path]

    __getitem__ = __getattr__

    def __call__(self, method, path, **kwargs):
        try:
            kwargs = self._merge_params(**kwargs)
            response = self._session.request(method, self.url_for(path), **kwargs)
            response.raise_for_status()
            return ApiResponse(response.status_code, response.json(object_hook=JsonObject))
        except HTTPError as e:
            raise ApiException(status=e.response.status_code, message=e.response.text)
        except Exception as e:
            raise ApiException(e)

    def _merge_params(self, **kwargs):
        if self.default_params:
            params = kwargs.pop('params', {}) or {}
            params.update(self.default_params)
            kwargs.update({'params': params})
        return kwargs

    @staticmethod
    def url_for(path):
        return str(path)


class OAuth2Api(Api):
    def __init__(self, base_url=None):
        import requests_oauthlib
        super(OAuth2Api, self).__init__(base_url, requests_oauthlib.OAuth2Session())

    def use_access_token(self, access_token, included_params=True):
        if access_token:
            self._session.token = {'access_token': access_token}
            if included_params:
                self.default_params.update(self._session.token)
        return self


class OAuth1Api(Api):
    def __init__(self, base_url=None, client_key=None, client_secret=None, resource_owner_key=None,
                 resource_owner_secret=None):
        import requests_oauthlib
        super(OAuth1Api, self).__init__(
            base_url,
            requests_oauthlib.OAuth1Session(
                client_key=client_key,
                client_secret=client_secret,
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret
            )
        )

    def use_key(self, client_key=None, client_secret=None, resource_owner_key=None, resource_owner_secret=None):
        self._session.client_key = client_key
        self._session.client_secret = client_secret
        self._session.resource_owner_key = resource_owner_key
        self._session.resource_owner_secret = resource_owner_secret
        return self
