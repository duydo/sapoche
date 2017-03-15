from sapoche.helpers.preconditions import check_not_empty
from sapoche.social_api.base import OAuth2Api

__author__ = 'duydo'


class Cursor(object):
    """Cursor-based pagination"""
    summary = {}
    _r = None
    _params = {'summary': True}

    def __init__(self, api, path, **kwargs):
        self._api = api
        self._path = path
        self._params.update(kwargs)

    def __iter__(self):
        return self

    def next(self):
        if self._r is None:
            self._r = self._path.get(self._params)
            if 'summary' in self._r.data:
                self.summary = self._r.data.summary
            return self._r.data.data

        if 'paging' in self._r.data and 'next' in self._r.data.paging:
            self._r = self._api[self._r.data.paging['next']].get()
            return self._r.data.data
        raise StopIteration


class Facebook(OAuth2Api):
    BASE_URL = 'https://graph.facebook.com'
    VERSION = 'v2.8'

    def __init__(self, token=None, version=None):
        super(Facebook, self).__init__('%s/%s' % (self.BASE_URL, version or self.VERSION))
        self.use_token(token)

    def node(self, node_id, **kwargs):
        return self[check_not_empty(node_id)].get(kwargs).data

    def graph(self, node_id='me', edge_name=None, **kwargs):
        return Cursor(self, self[check_not_empty(node_id)][check_not_empty(edge_name)], **kwargs)
