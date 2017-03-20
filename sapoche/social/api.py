import urlparse

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

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
    def __init__(self, message=None, status=None):
        self.status = status
        super(ApiException, self).__init__(unicode(message))

    def __str__(self):
        return '<%s [%s]' % (self.status, self.message)


class ApiResponse(object):
    """Represent response for API"""

    status = None
    meta = None
    body = None

    def __init__(self, status=None, body=None, meta=None):
        """
        :param status: HTTP status code
        :param body: JsonObject represents body of response
        :param meta: JsonObject represents meta data of response : url, headers, cookies
        """
        self.status = status
        self.body = body
        self.meta = meta

    @classmethod
    def from_response(cls, response):
        return cls(
            status=response.status_code,
            body=response.json(object_hook=JsonObject),
            meta=JsonObject({
                'url': response.url,
                'headers': response.headers,
                'reason': response.reason,
            })
        )

    def __repr__(self):
        return '<%s [%s]>' % (self.__class__.__name__, self.status)


class ApiPath(object):
    """ApiPath provides a convenient way to build API endpoint prepare for calling service APIs."""

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

    def __call__(self, params=None, data=None, method='GET', **kwargs):
        """Execute API request.
        :param method: HTTP method 
        :param params: (optional) Dictionary or bytes to be sent in the query
            string.
        :param data: (optional) Dictionary, bytes, or file-like object to send
            in the body of the request.
        :param kwargs: kwargs for Api.__call__ method.
        :rtype: ApiResponse
        """
        kwargs.update({'params': params, 'data': data})
        return self._api(method, self, **kwargs)


class Api(object):
    """Base Api class"""

    _auto_params = {}

    def __init__(self, base_url=None, session=None):
        self._base_url = self._check_and_normalize_base_url(base_url)
        self._session = session or self.create_default_session()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def __getattr__(self, path):
        return ApiPath(self, path)

    __getitem__ = __getattr__

    def __call__(self, method, path, **kwargs):
        """Execute the API request.
        
        :param method: A Http method, eg: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS  
        :param path: ApiPath object
        :param kwargs:
             :param params: (optional) Dictionary or bytes to be sent in the query
            string.
            :param data: (optional) Dictionary, bytes, or file-like object to send
            in the body of the request.
            json: (optional) json to send in the body of the request.
            headers: (optional) Dictionary of HTTP Headers to send with the request.
            cookies: (optional) Dict or CookieJar object to send with the request.
            files: (optional) Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
            auth: (optional) Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
            timeout: (optional) How long to wait for the server to send
                data before giving up, as a float, or a :ref:`(connect timeout,
                read timeout) <timeouts>` tuple.
            timeout: float or tuple
            allow_redirects: (optional) Set to True by default.
            allow_redirects: bool
            proxies: (optional) Dictionary mapping protocol or protocol and
                hostname to the URL of the proxy.
            stream: (optional) whether to immediately download the response
                content. Defaults to ``False``.
            verify: (optional) whether the SSL cert will be verified.
                A CA_BUNDLE path can also be provided. Defaults to ``True``.
            cert: (optional) if String, path to ssl client cert file (.pem).
                If Tuple, ('cert', 'key') pair.
        :rtype: ApiResponse
        """
        try:
            response = self._session.request(method, self.url_for(path), **kwargs)
            response.raise_for_status()
            return ApiResponse.from_response(response)
        except requests.HTTPError as e:
            self.handle_exception(ApiException(e.response.text, e.response.status_code))
        except Exception as e:
            self.handle_exception(ApiException(e))

    def _check_and_normalize_base_url(self, base_url):
        if self.is_absolute_url(base_url):
            return base_url if base_url.endswith('/') else '%s/' % base_url
        raise ValueError('base_url is invalid.')

    @staticmethod
    def is_absolute_url(url):
        return bool(urlparse.urlparse(url).netloc)

    @staticmethod
    def create_default_session():
        return requests.Session()

    def url_for(self, path):
        return urlparse.urljoin(self.base_url, str(path))

    def handle_exception(self, exception):
        raise exception

    @property
    def base_url(self):
        return self._base_url

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value
        self.on_session_set(self._session)
        return self

    def attach_params(self, **kwargs):
        """Attach custom params for all requests."""
        self._session.params.update(kwargs)
        return self

    def on_session_set(self, session):
        pass


class TokenPlace:
    AUTH_HEADER = 'auth_header'
    BODY = 'body'
    QUERY = 'query'


class SocialApi(Api):
    """SocialApi represents an API for all social network APIs using OAuth2 protocol.

    Usage:
    base_api_url = 'https://path-to-api-provider'
    access_token = 'yyy'
    api = SocialApi(base_api_url, access_token)

    r = api.foo() # endpoint /foo 
    print r.body 
    
    r = api.foo.bar() # endpoint foo/bar 
    print r.body 
    
    """

    def __init__(self, base_url=None, access_token=None, access_token_name=None, access_token_place=None):
        super(SocialApi, self).__init__(base_url)

        self._access_token_name = access_token_name or 'access_token'
        self._access_token_place = access_token_place
        self.session = self.create_oauth2_session(token_place=self._access_token_place)
        self.access_token = access_token

    def fetch_token(self, token_url=None, client_id=None, client_secret=None, **kwargs):
        check_not_empty(token_url)
        check_not_empty(client_id)
        check_not_empty(client_secret)
        if self._access_token_place == TokenPlace.AUTH_HEADER:
            return self.session.fetch_token(
                token_url=token_url,
                auth=HTTPBasicAuth(client_id, client_secret),
                **kwargs
            )
        return self.session.fetch_token(
            token_url=token_url,
            client_id=client_id,
            client_secret=client_secret,
            **kwargs
        )

    @staticmethod
    def create_oauth2_session(client=None, client_id=None, token_place=None, **kwargs):
        import requests_oauthlib
        return requests_oauthlib.OAuth2Session(
            client=client or BackendApplicationClient(client_id=client_id, default_token_placement=token_place),
            **kwargs
        )

    @property
    def access_token(self):
        return getattr(self.session, self._access_token_name, None)

    @access_token.setter
    def access_token(self, value):
        self.session.token = {self._access_token_name: check_not_empty(value)}
