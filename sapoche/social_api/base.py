import requests

from sapoche.helpers.preconditions import check_type, check_not_empty

__author__ = 'duydo'


class JsonObject(dict):
    """Read-only Json Object"""

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('Property "%s" not found in %s.' % (name, self.__class__.__name__))

    def __setattr__(self, *args):
        raise AttributeError('%s is read-only object.' % self.__class__.__name__)

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

    def __init__(self, base_url=None, session=None):
        self._base_url = check_not_empty(base_url)
        self._session = session or requests.Session()
        self._base_path = ApiPath(self, base_url)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __getattr__(self, path):
        if path.startswith(self._base_url):
            """This case happens when results have pagination links"""
            return ApiPath(self, path)
        return self._base_path[path]

    __getitem__ = __getattr__

    def __call__(self, method, path, **kwargs):
        try:
            _kwargs = self._merge_kwargs(**kwargs)
            response = self._session.request(method, self.url_for(path), **_kwargs)
            response.raise_for_status()
            return ApiResponse(response.status_code, response.json(object_hook=JsonObject))
        except requests.HTTPError as e:
            self.handle_exception(ApiException(e.response.text, e.response.status_code))
        except Exception as e:
            self.handle_exception(ApiException(e))

    def _merge_kwargs(self, **kwargs):
        if not self.default_params:
            return kwargs

        merged_kwargs = kwargs.copy()
        params = self.default_params.copy()
        params.update(kwargs.pop('params', {}) or {})
        merged_kwargs.update({'params': params})
        return merged_kwargs

    @staticmethod
    def url_for(path):
        return str(path)

    def handle_exception(self, api_exception):
        raise api_exception


class OAuth2Api(Api):
    def __init__(self, base_url=None):
        import requests_oauthlib
        super(OAuth2Api, self).__init__(base_url, requests_oauthlib.OAuth2Session())

    def use_access_token(self, access_token, included_in_params=True):
        if access_token:
            self._session.token = {'access_token': access_token}
            if included_in_params:
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
