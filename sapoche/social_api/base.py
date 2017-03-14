import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests import RequestException, HTTPError, Session
from requests_oauthlib import OAuth2Session

__author__ = 'duydo'


class JsonObject(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('%s has no property named %s.' % (self.__class__.__name__, name))

    def __setattr__(self, *args):
        raise AttributeError('%s instances are read-only.' % self.__class__.__name__)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, dict.__repr__(self))

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


class ApiPath(object):
    def __init__(self, api=None, path=None):
        self._api = api
        self._path = path

    def __getattr__(self, path):
        return self[path]

    def __getitem__(self, path):
        if self._path is not None:
            path = '%s/%s' % (self._path, path)
        return ApiPath(self._api, path)

    def __str__(self):
        return self._path

    def __repr__(self):
        return '<ApiPath: %s>' % self._path

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

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __getattr__(self, path):
        return ApiPath(self, path)

    __getitem__ = __getattr__

    def __call__(self, method, url, **kwargs):
        try:
            _url = str(url)
            _url = _url if _url.startswith(self._base_url) else '%s/%s' % (self._base_url, _url)
            response = self._session.request(method, _url, **kwargs)
            response.raise_for_status()
            return ApiResponse(response.status_code, response.json(object_hook=JsonObject))
        except HTTPError as e:
            raise ApiException(status=e.response.status_code, message=e.response.text)
        except Exception as e:
            print e
            raise ApiException(e)
