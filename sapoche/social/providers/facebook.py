import json

from sapoche.helpers import check_not_empty
from sapoche.social.api import SocialApi

__author__ = 'duydo'


class PagingIter(object):
    """Paging Iterator"""

    _page = 0

    def __init__(self, api, obj):
        self._api = api
        self._obj = obj

    def __iter__(self):
        return self

    def next(self):
        if self._page == 0:
            self._page += 1
            return self._obj.data, self._obj.paging

        if 'next' in self._obj.paging:
            r = self._api[self._obj.paging['next']].get()
            self._obj = r.data
            self._page += 1
            return self._obj.data, self._obj.paging
        raise StopIteration


class FacebookException(Exception):
    def __init__(self, api_exception):
        if api_exception and api_exception.message:
            self.message = api_exception.message
            msg = json.loads(self.message)
            self.__dict__.update(msg.get('error', {}))
        super(FacebookException, self).__init__(self.message)


class Facebook(SocialApi):
    """Facebook Graph API.
    See https://developers.facebook.com/docs/graph-api
    """

    BASE_GRAPH_API_URL = 'https://graph.facebook.com'
    VERSION = '2.8'

    def __init__(self, access_token=None, version=None):
        super(Facebook, self).__init__(
            base_url='%s/v%s' % (self.BASE_GRAPH_API_URL, version or self.VERSION),
            access_token=access_token
        )
        from requests_oauthlib.compliance_fixes.facebook import facebook_compliance_fix
        self.session = facebook_compliance_fix(self.session)

    def graph(self, node_id, fields=None, **kwargs):
        kwargs.update({'fields': fields})
        return self[check_not_empty(node_id)].get(kwargs).data

    def iter_paging(self, edge):
        """Paging Iterator"""
        return PagingIter(self, edge)

    def search(self, q, type='user', **kwargs):
        """Search API"""
        params = kwargs.copy()
        params.update({'q': check_not_empty(q), 'type': check_not_empty(type)})
        return self.iter(self['search'].get(params))

    def handle_exception(self, api_exception):
        raise FacebookException(api_exception)
