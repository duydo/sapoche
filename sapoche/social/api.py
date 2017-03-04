from requests import RequestException

__author__ = 'duydo'


class JsonObject(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('%s has no property named %s.' % (self.__class__.__name__, name))

    def __setattr__(self, *args):
        raise AttributeError('%s instances are read-only.' % self.__class__.__name__)

    __delattr__ = __setitem__ = __delitem__ = __setattr__

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, dict.__repr__(self))


class Api(object):
    def __init__(self, client, path=None):
        self._client = client
        self._path = path

    def __repr__(self):
        return '<ApiComponent: %s>' % self._path

    def __getitem__(self, path):
        if self._path is not None:
            path = '%s/%s' % (self._path, path)
        return Api(self._client, path)

    def __getattr__(self, path):
        return self[path]

    def get(self, **params):
        if self._path is None:
            raise TypeError('Calling get() on an empty API path is not supported.')
        return self._client.make_request('GET', self._path, **params)

    def post(self, **params):
        if self._path is None:
            raise TypeError('Calling post() on an empty API path is not supported.')
        return self._client.make_request('POST', self._path, **params)

    @property
    def path(self):
        return self._path


class ApiException(Exception):
    def __init__(self, reason=None, status_code=None, response=None):
        self.reason = unicode(reason)
        self.status_code = status_code
        self.response = response
        super(ApiException, self).__init__(reason)

    def __str__(self):
        return str(self.response.text) or self.reason


class ApiResponse(object):
    def __init__(self, response, method, data):
        self.url = response.url
        self.headers = response.headers
        self.method = method
        self.data = data


class ApiClient(object):
    base_url = None
    session = None

    _default_params = {}

    def __getattr__(self, path):
        return Api(self, path)

    def set_base_url(self, base_url):
        self.base_url = base_url
        return self

    def set_session(self, session):
        self.session = session
        return self

    def set_default_params(self, **params):
        self._default_params.update(params)
        return self

    def make_request(self, method, path, **params):
        try:
            method = method.upper()
            request_url = self._prepare_url(path)
            request_params = self._prepare_params(method, params)
            response = self._make_request(method, request_url, **request_params)
            if response.status_code == 200:
                return ApiResponse(response, method, response.json())
            self.raise_exceptions_for_status(response)
        except RequestException as e:
            raise ApiException(str(e))

    @staticmethod
    def raise_exceptions_for_status(response):
        error_msg = None
        if isinstance(response.reason, bytes):
            reason = response.reason.decode('utf-8', 'ignore')
        else:
            reason = response.reason
        status_code = response.status_code
        if 400 <= status_code < 500:
            error_msg = u'%s Client Error: %s for url: %s' % (status_code, reason, response.url)
        elif 500 <= status_code < 600:
            error_msg = u'%s Server Error: %s for url: %s' % (status_code, reason, response.url)
        if error_msg:
            raise ApiException(error_msg, status_code, response)

    def _prepare_url(self, path):
        paths = [_.replace('__', '.') for _ in path.split('/')]
        return '%s/%s' % (self.base_url, '/'.join(paths[1:]))

    def _make_request(self, method, url, **request_params):
        return self.session.request(method, url, **request_params)

    @staticmethod
    def json_object_hook(data):
        return JsonObject(data)

    def _prepare_params(self, method, params):
        _params, files = {}, {}
        if self._default_params:
            params.update(self._default_params)

        for k, v in params.items():
            if hasattr(v, 'read') and callable(v.read):
                files[k] = v
            elif isinstance(v, bool):
                _params[k] = 'true' if v else 'false'
            elif isinstance(v, list):
                _params[k] = ','.join(v)
            else:
                _params[k] = v

        request_params = {}
        if method == 'GET':
            request_params['params'] = _params
        elif method == 'POST':
            request_params['data'] = _params
            request_params['files'] = files
        return request_params


class OAuth1ApiClient(ApiClient):
    _consumer_key = None
    _consumer_secret = None
    _access_token_key = None
    _access_token_secret = None

    def set_auth(self, client_key, client_secret, access_token_key=None, access_token_secret=None):
        self._consumer_key = client_key
        self._consumer_secret = client_secret
        self._access_token_key = access_token_key
        self._access_token_secret = access_token_secret
        keys = [client_key, client_secret, access_token_key, access_token_secret]
        if all(keys):
            from requests_oauthlib import OAuth1Session
            self.set_session(OAuth1Session(
                client_key=client_key,
                client_secret=client_secret,
                resource_owner_key=access_token_key,
                resource_owner_secret=access_token_secret,
            ))


class OAuth2ApiClient(ApiClient):
    _client_id = None
    _client_secret = None

    def set_auth(self, client_id=None, client_secret=None):
        from requests_oauthlib import OAuth2Session
        from oauthlib.oauth2 import BackendApplicationClient
        self._client_id = client_id
        self._client_secret = client_secret
        self.set_session(OAuth2Session(client=BackendApplicationClient(client_id)))
