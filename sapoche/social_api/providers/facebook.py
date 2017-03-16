import json

from sapoche.helpers.preconditions import check_not_empty
from sapoche.social_api.base import OAuth2Api

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
            return self._obj.data

        if 'next' in self._obj.paging:
            r = self._api[self._obj.paging['next']].get()
            self._obj = r.data
            self._page += 1
            return self._obj.data
        raise StopIteration


class FacebookException(Exception):
    def __init__(self, api_exception):
        if api_exception and api_exception.message:
            self.message = api_exception.message
            msg = json.loads(self.message)
            self.__dict__.update(msg.get('error', {}))


class Facebook(OAuth2Api):
    """Simple Facebook Graph API Implementation.
    
    See https://developers.facebook.com
    
    Usage:
        fb = Facebook('<your access_token>')
        
        # You can get a Node/Object and its fields by using:
        r = fb.graph(node_id, fields)

        # Get name, about of a User by User ID
        user_id = ''
        
        r = fb.graph(user_id, fields='name,about')
        print r.name, r.about
        
        # or get edge friends
        r = fb.graph(user_id, fields='id,name,friends')
        print r.id, r.name #
        
        # Get all friends with page iterator
        for friends in fb.iter(r.friends):
            for friend in friends:
                print friend.id, friend.name
        
        
        
        
    """

    BASE_URL = 'https://graph.facebook.com'
    VERSION = 'v2.8'

    def __init__(self, access_token=None, version=None):
        super(Facebook, self).__init__('%s/%s' % (self.BASE_URL, version or self.VERSION))
        self.use_access_token(access_token)

    def node(self, node_id, fields=None, **kwargs):
        kwargs.update({'fields': fields})
        return self[check_not_empty(node_id)].get(kwargs).data

    def paging(self, edge):
        return PagingIter(self, edge)

    def search(self, q, type='user', **kwargs):
        """Search API"""
        params = kwargs.copy()
        params.update({'q': check_not_empty(q), 'type': check_not_empty(type)})
        return self.iter(self['search'].get(params))
