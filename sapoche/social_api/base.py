import requests
from requests import HTTPError
from requests_oauthlib import OAuth2Session

from sapoche.helpers.preconditions import check_type, check_not_none, check_not_empty

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
            response = self._session.request(method, self.url_for(path), **kwargs)
            response.raise_for_status()
            return ApiResponse(response.status_code, response.json(object_hook=JsonObject))
        except HTTPError as e:
            raise ApiException(status=e.response.status_code, message=e.response.text)
        except Exception as e:
            raise ApiException(e)

    @staticmethod
    def url_for(path):
        return str(path)


class OAuth2Api(Api):
    def __init__(self, base_url=None):
        super(OAuth2Api, self).__init__(base_url, OAuth2Session())

    def use_token(self, access_token):
        if access_token:
            self._session.token = {'access_token': access_token}
        return self
